import mysql.connector
from mysql.connector import Error
from core.db_connection import create_connection, close_connection
from datetime import datetime

print("="*60)
print("CRUD OPERATIONS - DATABASE MANAGEMENT")
print("="*60)

# ==================== CREATE OPERATIONS ====================

def insert_student(Name, Room_NO, Department, Join_Date):
    """
    INSERT - Add new student to database
    """
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO students (Name, Room_NO, Department, Join_Date)
        VALUES (%s, %s, %s, %s)
        """
        values = (Name, Room_NO, Department, Join_Date)
        cursor.execute(query, values)
        connection.commit()
        
        Student_ID = cursor.lastrowid
        print(f"Student added successfully! ID: {Student_ID}")
        return True
        
    except Error as e:
        print(f"Error inserting student: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def insert_attendance(Student_ID, Date, Meal_Type, Is_Present=1):
    """
    INSERT - Record student attendance
    """
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO daily_attendance (Student_ID, Date, Meal_Type, Is_Present)
        VALUES (%s, %s, %s, %s)
        """
        values = (Student_ID, Date, Meal_Type, Is_Present)
        cursor.execute(query, values)
        connection.commit()
        
        print(f"Attendance recorded for Student ID: {Student_ID}")
        return True
        
    except Error as e:
        print(f"Error recording attendance: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

# ==================== READ OPERATIONS ====================

def get_all_students():
    """
    SELECT - Get all students
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM students"
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f"\nFound {len(results)} students")
        return results
        
    except Error as e:
        print(f"Error fetching students: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

def get_student_by_id(Student_ID):
    """
    SELECT - Get specific student by ID
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        # Table column name is Student_ID
        query = "SELECT * FROM students WHERE Student_ID = %s"
        cursor.execute(query, (Student_ID,))
        result = cursor.fetchone()
        
        if result:
            print(f"Student found: {result['Name']}")
        else:
            print(f"No student found with ID: {Student_ID}")
        
        return result
        
    except Error as e:
        print(f"Error fetching student: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

def get_attendance_by_date(date):
    """
    SELECT - Get attendance for specific date
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        # Ensure column names match SQL Schema exactly (Name, Room_NO, Date, Meal_Type)
        query = """
        SELECT da.*, s.Name, s.Room_NO
        FROM daily_attendance da
        JOIN students s ON da.Student_ID = s.Student_ID
        WHERE da.Date = %s
        ORDER BY da.Meal_Type, s.Name
        """
        cursor.execute(query, (date,))
        results = cursor.fetchall()
        
        print(f"\nFound {len(results)} attendance records for {date}")
        return results
        
    except Error as e:
        print(f"Error fetching attendance: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

# ==================== UPDATE OPERATIONS ====================

def update_student(Student_ID, Name=None, Room_NO=None, Department=None):
    """
    UPDATE - Modify student information
    """
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        updates = []
        values = []
        
        if Name:
            updates.append("Name = %s")
            values.append(Name)
        if Room_NO:
            updates.append("Room_NO = %s")
            values.append(Room_NO)
        if Department:
            updates.append("Department = %s")
            values.append(Department)
        
        if not updates:
            print("No fields to update")
            return False
        
        values.append(Student_ID)
        # Table column name is Student_ID
        query = f"UPDATE students SET {', '.join(updates)} WHERE Student_ID = %s"
        
        cursor.execute(query, tuple(values))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Student ID {Student_ID} updated successfully")
            return True
        else:
            # Check if student exists but data was identical
            check_cursor = connection.cursor()
            check_cursor.execute("SELECT Student_ID FROM students WHERE Student_ID = %s", (Student_ID,))
            if check_cursor.fetchone():
                print(f"Student ID {Student_ID} exists, but no changes were made (Same data).")
                return True
            else:
                print(f"No student found with ID: {Student_ID}")
                return False
        
    except Error as e:
        print(f"Error updating student: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def update_attendance(Attendance_ID, Is_Present):
    """
    UPDATE - Modify attendance status
    """
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        # Table column is Attendance_ID and Is_Present
        query = "UPDATE daily_attendance SET Is_Present = %s WHERE Attendance_ID = %s"
        cursor.execute(query, (Is_Present, Attendance_ID))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Attendance ID {Attendance_ID} updated")
            return True
        else:
            print(f"No attendance found or no changes made for ID: {Attendance_ID}")
            return False
        
    except Error as e:
        print(f"Error updating attendance: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

# ==================== DELETE OPERATIONS ====================

def delete_student(Student_ID):
    """
    DELETE - Remove student from database
    """
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "DELETE FROM students WHERE Student_ID = %s"
        cursor.execute(query, (Student_ID,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Student ID {Student_ID} deleted successfully")
            return True
        else:
            print(f"No student found with ID: {Student_ID}")
            return False
        
    except Error as e:
        print(f"Error deleting student: {e}")
        print("    (Student may have attendance records - delete those first)")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def delete_attendance(Attendance_ID):
    """
    DELETE - Remove attendance record
    """
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "DELETE FROM daily_attendance WHERE Attendance_ID = %s"
        cursor.execute(query, (Attendance_ID,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Attendance ID {Attendance_ID} deleted")
            return True
        else:
            print(f"No attendance found with ID: {Attendance_ID}")
            return False
        
    except Error as e:
        print(f"Error deleting attendance: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

# ==================== DEMO / TESTING ====================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING CRUD OPERATIONS")
    print("="*60)
    
    # 1. CREATE
    print("\n1️⃣ CREATE - Adding new student...")
    insert_student("Test Student", "999Z", "CSE", "2026-02-01")
    
    # 2. READ ALL
    print("\n2️⃣ READ - Getting all students...")
    students = get_all_students()
    if students:
        for student in students[:3]:
            # Keys must match SQL: Student_ID, Name, Room_NO, Department, Join_Date
            print(f"   ID: {student['Student_ID']}")
            print(f"   Name: {student['Name']}")
            print(f"   Room: {student['Room_NO']}")
            print(f"   Department: {student['Department']}")
            print(f"   Join Date: {student['Join_Date']}")
            print("-" * 40)
    
    # 3. READ ONE
    print("\n3️⃣ READ - Getting student by ID...")
    student = get_student_by_id(1)
    if student:
        print(f"   {student}")
    
    # 4. UPDATE
    print("\n4️⃣ UPDATE - Updating student room number...")
    update_student(1, Room_NO="101B")
    
    # 5. READ (Verify)
    print("\n5️⃣ READ - Verifying update...")
    get_student_by_id(1)
    
    # 6. READ ATTENDANCE
    print("\n6️⃣ READ - Getting attendance for 2024-12-25...")
    attendance = get_attendance_by_date("2024-12-25")
    if attendance:
        for record in attendance[:3]:
            # Keys match SQL: Name, Meal_Type, Is_Present
            print(f"   Student: {record['Name']}, Meal: {record['Meal_Type']}, Present: {record['Is_Present']}")
    
    print("\n" + "="*60)
    print("CRUD OPERATIONS TEST COMPLETE")
    print("="*60)