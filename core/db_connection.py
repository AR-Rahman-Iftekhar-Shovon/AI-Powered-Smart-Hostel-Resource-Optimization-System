import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Create a database connection to MySQL
    Returns connection object if successful, None otherwise
    """
    try:
        try:
            from core.config import DB_CONFIG
            connection = mysql.connector.connect(**DB_CONFIG)
        except ImportError:
            # If config.py doesn't exist, use manual input
            print("config.py not found!")
            print("Please create core/config.py with your database credentials")
            print("See README.md for instructions")
            return None
        
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
            
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    """
    Close database connection
    """
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed")

# Test the connection
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        close_connection(conn)