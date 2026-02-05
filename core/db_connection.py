import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Create a database connection to MySQL
    Returns connection object if successful, None otherwise
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='smart_hostel_db',
            user='root',
            password='Shovon@21'  
        )
        
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