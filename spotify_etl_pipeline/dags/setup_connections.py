"""Run this once to set up Airflow connections
Execute: docker exec spotify_etl_pipeline-airflow-webserver-1 python /opt/airflow/dags/setup_connections.py"""
from airflow.models import Connection
from airflow import settings
import os

def setup_connections():
    spotify_conn = Connection(
        conn_id='spotify_postgres',
        conn_type='postgres',
        host='host.docker.internal'
        port='5433',
        schema='spotify_data',
        login='postgres',
        password='postgres',
        extra='{"sslmode": "disable"}'
    )
    
    session = settings.Session()
    
    # Delete if exists
    existing = session.query(Connection).filter(Connection.conn_id == 'spotify_postgres').first()
    if existing:
        session.delete(existing)
    
    # Add new connection
    session.add(spotify_conn)
    session.commit()
    
    print(" Connection 'spotify_postgres' created successfully!")
    print(f"   Host: host.docker.internal")
    print(f"   Port: 5433")
    print(f"   Database: spotify_data")

if __name__ == "__main__":
    setup_connections()
