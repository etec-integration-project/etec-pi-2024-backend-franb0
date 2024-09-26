import os
import pymysql

# Set environment variables (for testing, you can set them directly here)
os.environ['DATABASE_HOST'] = 'mysql'
os.environ['DATABASE_USERNAME'] = 'root'
os.environ['DATABASE_PASSWORD'] = 'root'
os.environ['DATABASE_NAME'] = 'app'  # or whatever your DB name is

try:
    connection = pymysql.connect(
        host=os.environ['DATABASE_HOST'],
        user=os.environ['DATABASE_USERNAME'],
        password=os.environ['DATABASE_PASSWORD'],
        database=os.environ['DATABASE_NAME']
    )

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(result)

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals():
        connection.close()
