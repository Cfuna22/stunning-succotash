from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from extract_spotify import SpotifyExtractor
import pandas as pd
import logging

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'Cfuna22',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2023, 12, 22),
}

def extract_spotify_data(**context):
    """Extract data from Spotify API"""
    logger.info('Starting Spotify data extraction...')

    try:
        extractor = SpotifyExtractor()

        # Get user profile
        profile = extractor.get_user_profile()
        logger.info(f'Extracted profile: {profile['display_name'] if profile else 'No profile'}')

        # Get recently played tracks (last 50)
        tracks_df = extractor.get_recent_played(limit=50)
        logger.info(f'Extracted {len(tracks_df)} recently played tracks')

        # Get top tracks for all time ranges
        time_range = ['short_term', 'medium_term', 'long_term']
        top_tracks_data = {}

        for time_range in time_ranges:
            top_tracks = extractor.get_top_tracks(time_range=time_range, limit=20)
            top_tracks_data[time_range] = top_tracks
            logger.info(f'Extracted {len(top_tracks)} top tracks form {time_range}')

            # Push data to XCom for use in other tasks
            context['ti'].xcom_push(key='user_profile', value=profile)
            context['ti'].xcom_push(key='recent_tracks', value=tracks_df.to_dict('records'))
            context['ti'].xcom_push(key='top_tracks_data', value={
                k: v.to_dict('records') for k, v in top_tracks_data.items()
            })

            return {
                'status': 'success',
                'profile_extracted': profile is not None,
                'tracks_extracted': len(tracks_df),
                'top_tracks_extracted': {k: len(v) for k, v in top_tracks_data.items()}
            }

    except Exception as e:
        logger.error(f'Extraction failed: {e}')
        raise

def transform_data(**context):
    """Transform and clean the data"""
    logger.info("Starting data transformation...")
    
    try:
        # Pull data from previous task via XCom
        ti = context['ti']
        profile = ti.xcom_pull(task_ids='extract_data', key='user_profile')
        recent_tracks = ti.xcom_pull(task_ids='extract_data', key='recent_tracks')
        
        if not profile:
            logger.warning("No profile data to transform")
            return {'status': 'skipped', 'reason': 'No profile data'}
        
        # Transform profile data
        transformed_profile = {
            'user_id': profile['user_id'],
            'display_name': profile['display_name'],
            'email': profile.get('email', ''),
            'country': profile.get('country', ''),
            'followers': profile['followers'],
            'account_type': profile['account_type'],
            'etl_timestamp': datetime.now()
        }
        
        # Transform tracks data
        transformed_tracks = []
        if recent_tracks:
            for track in recent_tracks:
                transformed_track = {
                    'track_id': track['track_id'],
                    'track_name': track['track_name'],
                    'artist_id': track['artist_id'],
                    'artist_name': track['artist_name'],
                    'album_id': track.get('album_id', ''),
                    'album_name': track.get('album_name', ''),
                    'duration_ms': track['duration_ms'],
                    'popularity': track.get('popularity', 0),
                    'played_at': track['played_at'],
                    'etl_timestamp': datetime.now()
                }
                transformed_tracks.append(transformed_track)
        
        # Push transformed data
        ti.xcom_push(key='transformed_profile', value=transformed_profile)
        ti.xcom_push(key='transformed_tracks', value=transformed_tracks)
        
        logger.info(f"Transformed profile and {len(transformed_tracks)} tracks")
        return {'status': 'success', 'tracks_transformed': len(transformed_tracks)}
        
    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        raise

def load_to_postgres(**context):
    """Load data to PostgreSQL"""
    logger.info("Starting data load to PostgreSQL...")
    
    try:
        ti = context['ti']
        profile = ti.xcom_pull(task_ids='transform_data', key='transformed_profile')
        tracks = ti.xcom_pull(task_ids='transform_data', key='transformed_tracks')
        
        if not profile:
            logger.warning("No data to load")
            return {'status': 'skipped'}
        
        # Connect to PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id='spotify_postgres')
        connection = pg_hook.get_conn()
        cursor = connection.cursor()
        
        # Load user profile
        cursor.execute("""
            INSERT INTO users (user_id, display_name, email, country, followers, account_type, etl_timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                display_name = EXCLUDED.display_name,
                email = EXCLUDED.email,
                country = EXCLUDED.country,
                followers = EXCLUDED.followers,
                account_type = EXCLUDED.account_type,
                etl_timestamp = EXCLUDED.etl_timestamp
        """, (
            profile['user_id'],
            profile['display_name'],
            profile['email'],
            profile['country'],
            profile['followers'],
            profile['account_type'],
            profile['etl_timestamp']
        ))
        
        # Load tracks if available
        tracks_loaded = 0
        if tracks:
            for track in tracks:
                # Insert artist
                cursor.execute("""
                    INSERT INTO artists (artist_id, artist_name)
                    VALUES (%s, %s)
                    ON CONFLICT (artist_id) DO NOTHING
                """, (track['artist_id'], track['artist_name']))
                
                # Insert track
                cursor.execute("""
                    INSERT INTO tracks (track_id, track_name, artist_id, duration_ms, popularity)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (track_id) DO NOTHING
                """, (
                    track['track_id'],
                    track['track_name'],
                    track['artist_id'],
                    track['duration_ms'],
                    track['popularity']
                ))
                
                # Insert listening history
                cursor.execute("""
                    INSERT INTO listening_history (user_id, track_id, played_at, context_type)
                    VALUES (%s, %s, %s, %s)
                """, (
                    profile['user_id'],
                    track['track_id'],
                    track['played_at'],
                    'recently_played'
                ))
                
                tracks_loaded += 1
        
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info(f" Loaded profile and {tracks_loaded} tracks to PostgreSQL")
        return {'status': 'success', 'tracks_loaded': tracks_loaded}
        
    except Exception as e:
        logger.error(f"Load failed: {e}")
        raise

def data_quality_check(**context):
    """Run data quality checks"""
    logger.info("Running data quality checks...")
    
    try:
        pg_hook = PostgresHook(postgres_conn_id='spotify_postgres')
        
        # Check 1: User exists in database
        user_check = pg_hook.get_first("""
            SELECT COUNT(*) FROM users WHERE user_id = %s
        """, ('Cfuna22',))  # Replace with actual user ID
        
        # Check 2: Recent tracks were loaded
        tracks_check = pg_hook.get_first("""
            SELECT COUNT(*) FROM listening_history 
            WHERE played_at > NOW() - INTERVAL '7 days'
        """)
        
        logger.info(f"Data quality check results:")
        logger.info(f"  - User exists: {user_check[0] > 0}")
        logger.info(f"  - Recent tracks: {tracks_check[0]}")
        
        return {
            'status': 'success',
            'user_exists': user_check[0] > 0,
            'recent_tracks_count': tracks_check[0]
        }
        
    except Exception as e:
        logger.error(f"Data quality check failed: {e}")
        raise

# Define the DAG
with DAG(
    'spotify_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for Spotify data',
    schedule_interval='@daily',  # Run once per day
    catchup=False,
    tags=['spotify', 'etl', 'music']
) as dag:
    
    start = EmptyOperator(task_id='start')
    
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_spotify_data,
        provide_context=True,
    )
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True,
    )
    
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_to_postgres,
        provide_context=True,
    )
    
    quality_check_task = PythonOperator(
        task_id='data_quality_check',
        python_callable=data_quality_check,
        provide_context=True,
    )
    
    end = EmptyOperator(task_id='end')
    
    # Define workflow
    start >> extract_task >> transform_task >> load_task >> quality_check_task >> end

