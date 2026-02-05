import pandas as pd
from core.db_connection import create_connection, close_connection

def fetch_attendance_data():
    """
    Fetch daily attendance data from database
    Returns pandas DataFrame with attendance records
    """
    connection = create_connection()
    
    if connection is None:
        print("Failed to connect to database")
        return None
    
    try:
        query = """
        SELECT 
            da.date,
            da.meal_type,
            COUNT(CASE WHEN da.is_present = 1 THEN 1 END) as students_present,
            DAYNAME(da.date) as day_of_week,
            CASE 
                WHEN DAYOFWEEK(da.date) IN (1, 7) THEN 1 
                ELSE 0 
            END as is_weekend
        FROM daily_attendance da
        GROUP BY da.date, da.meal_type
        ORDER BY da.date, da.meal_type
        """
        
        df = pd.read_sql(query, connection)
        print(f"Successfully fetched {len(df)} records from database")
        print(f"\nData preview:")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
        
    finally:
        close_connection(connection)

def fetch_special_events():
    """
    Fetch special events data
    Returns pandas DataFrame with events
    """
    connection = create_connection()
    
    if connection is None:
        return None
    
    try:
        query = "SELECT * FROM special_events"
        df = pd.read_sql(query, connection)
        print(f"Fetched {len(df)} special events")
        return df
        
    except Exception as e:
        print(f"Error fetching events: {e}")
        return None
        
    finally:
        close_connection(connection)

# Test the data loader
if __name__ == "__main__":
    print("Testing data loader...\n")
    
    # Fetch attendance data
    attendance_df = fetch_attendance_data()
    
    print("\n" + "="*50 + "\n")
    
    # Fetch events data
    events_df = fetch_special_events()
    
    if attendance_df is not None:
        print(f"\nTotal records: {len(attendance_df)}")
        print(f"Date range: {attendance_df['date'].min()} to {attendance_df['date'].max()}")