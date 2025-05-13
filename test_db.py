import mysql.connector
import sys

def test_connection():
    try:
        connection = mysql.connector.connect(
            host='johntest.mysql.pythonanywhere-services.com',
            database='johntest$default',
            user='johntest',
            password='agrilink@123',
            port='3306'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"Connected to database: {record}")
            return True
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    test_connection()