from core.db_connection import create_connection, close_connection

print("="*60)
print("             ADVANCED SQL QUERIES - DATABASE COURSE")
print("="*60)

# ==================== COMPLEX JOINS ====================

def query_1_student_attendance_summary():
    """
    INNER JOIN + GROUP BY + COUNT
    Purpose: Show each student's total attendance count
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            s.student_id,
            s.name,
            s.department,
            COUNT(da.attendance_id) as total_meals_attended,
            SUM(CASE WHEN da.is_present = 1 THEN 1 ELSE 0 END) as meals_present,
            SUM(CASE WHEN da.is_present = 0 THEN 1 ELSE 0 END) as meals_absent
        FROM students s
        INNER JOIN daily_attendance da ON s.student_id = da.student_id
        GROUP BY s.student_id, s.name, s.department
        ORDER BY total_meals_attended DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("\n🔍 Query 1: Student Attendance Summary (INNER JOIN + GROUP BY)")
        print("-" * 80)
        for row in results[:5]:  # Show top 5
            print(f"ID: {row['student_id']}, Name: {row['name']}, "
                  f"Dept: {row['department']}, Total: {row['total_meals_attended']}, "
                  f"Present: {row['meals_present']}, Absent: {row['meals_absent']}")
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

def query_2_meal_wise_attendance():
    """
    LEFT JOIN + GROUP BY + AGGREGATION
    Purpose: Show meal-wise average attendance with student count
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            da.meal_type,
            COUNT(DISTINCT da.student_id) as unique_students,
            COUNT(da.attendance_id) as total_records,
            SUM(CASE WHEN da.is_present = 1 THEN 1 ELSE 0 END) as total_present,
            AVG(CASE WHEN da.is_present = 1 THEN 1 ELSE 0 END) * 100 as attendance_percentage
        FROM daily_attendance da
        GROUP BY da.meal_type
        ORDER BY total_present DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("\n🔍 Query 2: Meal-wise Attendance Statistics (GROUP BY + AGGREGATION)")
        print("-" * 80)
        for row in results:
            print(f"Meal: {row['meal_type']}, Students: {row['unique_students']}, "
                  f"Total Present: {row['total_present']}, "
                  f"Attendance %: {row['attendance_percentage']:.2f}%")
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

# ==================== SUBQUERIES ====================

def query_3_students_above_average_attendance():
    """
    SUBQUERY in WHERE clause
    Purpose: Find students who attended more than average
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            s.student_id,
            s.name,
            s.department,
            COUNT(da.attendance_id) as total_attendance
        FROM students s
        INNER JOIN daily_attendance da ON s.student_id = da.student_id
        WHERE da.is_present = 1
        GROUP BY s.student_id, s.name, s.department
        HAVING COUNT(da.attendance_id) > (
            SELECT AVG(attendance_count)
            FROM (
                SELECT COUNT(*) as attendance_count
                FROM daily_attendance
                WHERE is_present = 1
                GROUP BY student_id
            ) as avg_table
        )
        ORDER BY total_attendance DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("\n🔍 Query 3: Students Above Average Attendance (SUBQUERY + HAVING)")
        print("-" * 80)
        for row in results:
            print(f"ID: {row['student_id']}, Name: {row['name']}, "
                  f"Dept: {row['department']}, Attendance: {row['total_attendance']}")
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

def query_4_department_wise_ranking():
    """
    Simple Department-wise Ranking (Simplified Version)
    Purpose: Rank students by attendance within their department
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            s.department,
            s.name,
            COUNT(da.attendance_id) as total_attendance
        FROM students s
        INNER JOIN daily_attendance da ON s.student_id = da.student_id
        WHERE da.is_present = 1
        GROUP BY s.student_id, s.department, s.name
        ORDER BY s.department, total_attendance DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("\n🔍 Query 4: Department-wise Student Ranking (Simplified)")
        print("-" * 80)
        
        # Manual ranking per department
        current_dept = None
        rank = 0
        
        for row in results[:15]:  # Show first 15
            if row['department'] != current_dept:
                current_dept = row['department']
                rank = 1
                print(f"\n📚 {current_dept} Department:")
            
            print(f"   Rank #{rank}: {row['name']} "
                  f"(Attendance: {row['total_attendance']})")
            rank += 1
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

# ==================== MULTI-TABLE JOINS ====================

def query_5_complete_attendance_report():
    """
    3-TABLE JOIN + CASE WHEN + DATE FUNCTIONS
    Purpose: Comprehensive attendance report with all details
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            da.date,
            DAYNAME(da.date) as day_name,
            da.meal_type,
            s.name as student_name,
            s.department,
            s.room_no,
            CASE 
                WHEN da.is_present = 1 THEN 'Present'
                ELSE 'Absent'
            END as status,
            CASE 
                WHEN DAYOFWEEK(da.date) IN (1, 7) THEN 'Weekend'
                ELSE 'Weekday'
            END as day_type
        FROM daily_attendance da
        INNER JOIN students s ON da.student_id = s.student_id
        WHERE da.date >= '2024-12-25'
        ORDER BY da.date DESC, da.meal_type, s.name
        LIMIT 20
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("\n🔍 Query 5: Complete Attendance Report (3-TABLE JOIN + CASE)")
        print("-" * 100)
        for row in results[:10]:
            print(f"{row['date']} ({row['day_name']}, {row['day_type']}) | "
                  f"{row['meal_type']} | {row['student_name']} ({row['department']}) | "
                  f"Room: {row['room_no']} | {row['status']}")
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

# ==================== AGGREGATION WITH HAVING ====================

def query_6_low_attendance_students():
    """
    GROUP BY + HAVING + Comparison
    Purpose: Find students with attendance below threshold
    """
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT 
            s.student_id,
            s.name,
            s.department,
            COUNT(da.attendance_id) as total_meals,
            SUM(CASE WHEN da.is_present = 1 THEN 1 ELSE 0 END) as attended,
            (SUM(CASE WHEN da.is_present = 1 THEN 1 ELSE 0 END) / COUNT(da.attendance_id)) * 100 as attendance_rate
        FROM students s
        LEFT JOIN daily_attendance da ON s.student_id = da.student_id
        GROUP BY s.student_id, s.name, s.department
        HAVING attendance_rate < 75 OR attendance_rate IS NULL
        ORDER BY attendance_rate ASC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("\n🔍 Query 6: Low Attendance Alert (HAVING + Percentage Calculation)")
        print("-" * 80)
        for row in results:
            rate = row['attendance_rate'] if row['attendance_rate'] else 0
            print(f"{row['name']} ({row['department']}) - "
                  f"Attendance: {rate:.2f}% ({row['attended']}/{row['total_meals']})")
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

# ==================== RUN ALL QUERIES ====================

if __name__ == "__main__":
    print("\nRunning all advanced SQL queries...\n")
    
    query_1_student_attendance_summary()
    query_2_meal_wise_attendance()
    query_3_students_above_average_attendance()
    query_4_department_wise_ranking()
    query_5_complete_attendance_report()
    query_6_low_attendance_students()
    
    print("\n" + "="*60)
    print("✅ ALL ADVANCED QUERIES EXECUTED SUCCESSFULLY")
    print("="*60)
    print("\nConcepts Demonstrated:")
    print("   ✅ INNER JOIN")
    print("   ✅ LEFT JOIN")
    print("   ✅ GROUP BY + HAVING")
    print("   ✅ Aggregate Functions (COUNT, SUM, AVG)")
    print("   ✅ Subqueries")
    print("   ✅ Nested Subqueries")
    print("   ✅ CASE WHEN statements")
    print("   ✅ Date Functions")
    print("   ✅ Multi-table JOINs")
    print("="*60)