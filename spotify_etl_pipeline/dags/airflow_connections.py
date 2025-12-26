from airflow.models import Connection
from airflow import settings

spotify_conn = Connection(
    conn_id='spotify_postgres',
    conn_type='postgres',
    host='host.docker.internal',
    port='5433',
    schema='spotify_data',
    login='postgres',
    password='postgres',
    extra='{"sslmode": "disable"}'
)

session = settings.Session()
session.add(spotify_conn)
session.commit()
