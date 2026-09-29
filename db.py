import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mysql@#mahesh098",   # replace with the password you set during MySQL install
            database="library_db"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None