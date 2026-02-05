import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='smart_hostel_db',
            user='root',
            password='Shovon@21'
        )
        if connection.is_connected():
            print("Connected to MySQL")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def load_attendance_to_dataframe():
    connection = get_db_connection()
    if connection is None:
        return None
    
    query = """
    SELECT 
        da.date,
        da.meal_type,
        COUNT(da.student_id) AS students_present,
        COUNT(CASE WHEN da.is_present = 1 THEN 1 END) AS actual_attended
    FROM daily_attendance da
    GROUP BY da.date, da.meal_type
    ORDER BY da.date, da.meal_type
    """
    
    try:
        df = pd.read_sql(query, connection)
        print("\nAttendance Summary DataFrame:")
        print(df.head(10)) 
        print(f"\nTotal rows: {len(df)}")
        
        # Use relative path
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)   # auto-create folder if missing
        output_path = os.path.join(output_dir, "attendance_summary.csv")
        
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        
        return df
    
    except Error as e:
        print(f"Query error: {e}")
        return None
    
    finally:
        if connection.is_connected():
            connection.close()
            print("Connection closed")

if __name__ == "__main__":
    df = load_attendance_to_dataframe()