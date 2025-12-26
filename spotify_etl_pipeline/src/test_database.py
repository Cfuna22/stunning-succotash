import psycopg2
import sys

def test_connection():
    try:
        # Try to connect with the configuration
        connection = psycopg2.connect(
            host='localhost',
            port='5433',
            database='spotify_data',
            user='postgres',
            password='postgres'
        )

        cursor = connection.cursor()

        # Check PostgreSQL version
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]

        # Check if we can create a table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                test_message VARCHAR(100)
            )
        """)

        # Insert test data
        cursor.execute("INSERT INTO test_table (test_message) VALUE (%s)",
                      ('PostgreSQL connection successful!',))

        # Read it back
        cursor.execute('SELECT * FROM test_table')
        result = cursor.fetchone()

        print(' Postgres Connection Test:')
        print(f' Version: {version}')
        print(f' Test Result: {result[1]}')

        connection.commit()
        cursor.close()
        connection.close()

        return True

    except Exception as e:
        print(f' Connection failed: {e}')

if __name__ == '__main__':
    test_connection()
