# Database Design Documentation
## AI-Driven Smart Hostel Resource Optimization System

---

## 1. Database Overview

**Database Name:** `smart_hostel_db`  
**DBMS:** MySQL  
**Purpose:** Store hostel attendance data, student information, and ML predictions for resource optimization

---

## 2. Entity-Relationship (ER) Diagram
```
┌─────────────┐          ┌──────────────────┐          ┌─────────────────────┐
│  STUDENTS   │          │ DAILY_ATTENDANCE │          │ DAILY_MEAL_SUMMARY  │
├─────────────┤          ├──────────────────┤          ├─────────────────────┤
│ student_id  │◄────┐    │ attendance_id    │          │ summary_id          │
│ name        │     │    │ student_id (FK)  │          │ date                │
│ room_no     │     └────│ date             │          │ meal_type           │
│ department  │          │ meal_type        │          │ total_present       │
│ join_date   │          │ is_present       │          │ predicted_students  │
└─────────────┘          │ recorded_at      │          │ prediction_model    │
                         └──────────────────┘          │ confidence_score    │
                                                        └─────────────────────┘

                         ┌──────────────────┐
                         │ SPECIAL_EVENTS   │
                         ├──────────────────┤
                         │ event_id         │
                         │ event_date       │
                         │ event_name       │
                         │ impact_factor    │
                         │ description      │
                         └──────────────────┘
```

---

## 3. Table Schemas

### 3.1 Students Table

**Purpose:** Store basic information about hostel residents
```sql
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    room_no VARCHAR(20),
    department VARCHAR(50),
    join_date DATE
);
```

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| student_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique student identifier |
| name | VARCHAR(100) | NULL | Student's full name |
| room_no | VARCHAR(20) | NULL | Room number |
| department | VARCHAR(50) | NULL | Academic department |
| join_date | DATE | NULL | Date joined hostel |

---

### 3.2 Daily Attendance Table

**Purpose:** Track individual student meal attendance records
```sql
CREATE TABLE daily_attendance (
    attendance_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    date DATE NOT NULL,
    meal_type ENUM('Breakfast', 'Lunch', 'Dinner') NOT NULL,
    is_present TINYINT(1) DEFAULT 1,
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (student_id, date, meal_type),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| attendance_id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Unique attendance record ID |
| student_id | INT | FOREIGN KEY, NOT NULL | Reference to students table |
| date | DATE | NOT NULL | Date of meal |
| meal_type | ENUM | NOT NULL | Breakfast/Lunch/Dinner |
| is_present | TINYINT(1) | DEFAULT 1 | 1=Present, 0=Absent |
| recorded_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Timestamp of record |

**Constraints:**
- UNIQUE constraint on (student_id, date, meal_type) prevents duplicate entries
- Foreign key maintains referential integrity

---

### 3.3 Daily Meal Summary Table

**Purpose:** Store aggregated meal data and ML predictions
```sql
CREATE TABLE daily_meal_summary (
    summary_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    meal_type ENUM('Breakfast', 'Lunch', 'Dinner') NOT NULL,
    total_present INT NOT NULL,
    food_prepared_kg DECIMAL(8,2),
    food_consumed_kg DECIMAL(8,2),
    wastage_kg DECIMAL(8,2),
    predicted_students INT,
    prediction_model VARCHAR(50),
    confidence_score DECIMAL(5,4),
    decision_quantity DECIMAL(8,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (date, meal_type)
);
```

| Column | Data Type | Description |
|--------|-----------|-------------|
| summary_id | BIGINT | Unique summary ID |
| date | DATE | Date of meal |
| meal_type | ENUM | Meal type |
| total_present | INT | Actual students attended |
| predicted_students | INT | ML prediction |
| prediction_model | VARCHAR(50) | Model name used |
| confidence_score | DECIMAL(5,4) | Prediction confidence |

---

### 3.4 Special Events Table

**Purpose:** Store contextual factors affecting attendance
```sql
CREATE TABLE special_events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_date DATE NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    impact_factor DECIMAL(3,2) DEFAULT 1.00,
    description TEXT
);
```

---

## 4. Normalization

### 4.1 First Normal Form (1NF)
- All attributes contain atomic values  
- No repeating groups  
- Each column contains single value

### 4.2 Second Normal Form (2NF)
- Meets 1NF requirements  
- No partial dependencies  
- Non-key attributes fully dependent on primary key

### 4.3 Third Normal Form (3NF)
- Meets 2NF requirements  
- No transitive dependencies  
- Non-key attributes depend only on primary key

**Example:** Student name is stored in `students` table, not repeated in `daily_attendance`

---

## 5. Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| Students → Daily Attendance | One-to-Many | One student can have multiple attendance records |
| Daily Attendance → Daily Meal Summary | Aggregated | Attendance records summarized per day/meal |
| Special Events → Daily Attendance | Contextual | Events influence attendance patterns |

---

## 6. Indexes

**Primary Keys (Automatically Indexed):**
- `students(student_id)`
- `daily_attendance(attendance_id)`
- `daily_meal_summary(summary_id)`
- `special_events(event_id)`

**Composite Unique Indexes:**
- `daily_attendance(student_id, date, meal_type)` - Prevents duplicate entries
- `daily_meal_summary(date, meal_type)` - One summary per day/meal

**Foreign Key Index:**
- `daily_attendance(student_id)` - Fast lookups for student attendance

---

## 7. Database Operations Implemented

### 7.1 CRUD Operations (`core/crud_operations.py`)

| Operation | Implementation | Purpose |
|-----------|----------------|---------|
| **CREATE** | `INSERT INTO students/daily_attendance` | Add new records |
| **READ** | `SELECT` with various filters | Retrieve data |
| **UPDATE** | `UPDATE students/daily_attendance` | Modify existing data |
| **DELETE** | `DELETE FROM` with constraints | Remove records |

### 7.2 Advanced Queries (`core/advanced_queries.py`)

| Query Type | Concept | Purpose |
|------------|---------|---------|
| **JOIN** | INNER JOIN, LEFT JOIN | Combine multiple tables |
| **GROUP BY** | Aggregation | Summarize data |
| **HAVING** | Filter aggregated results | Find patterns |
| **Subquery** | Nested SELECT | Complex filtering |
| **CASE WHEN** | Conditional logic | Dynamic categorization |

---

## 8. Data Integrity

### 8.1 Constraints
- **PRIMARY KEY:** Ensures unique identification
- **FOREIGN KEY:** Maintains referential integrity
- **UNIQUE:** Prevents duplicate attendance entries
- **NOT NULL:** Ensures critical data presence
- **DEFAULT:** Automatic value assignment

### 8.2 Referential Integrity
- Cannot delete student if attendance records exist
- Cascading updates maintain consistency

---

## 9. Database Integration with Python

**Technology:** `mysql-connector-python`

**Connection Module:** `core/db_connection.py`
- Establishes MySQL connection
- Handles connection pooling
- Error management

**Data Pipeline:**
1. Python fetches data from MySQL
2. pandas converts to DataFrame
3. ML model trains on processed data
4. Predictions stored back in database

---

## 10. Sample Queries

### Get Student Attendance Summary
```sql
SELECT 
    s.name, 
    COUNT(da.attendance_id) as total_attendance
FROM students s
JOIN daily_attendance da ON s.student_id = da.student_id
WHERE da.is_present = 1
GROUP BY s.student_id;
```

### Find Low Attendance Students
```sql
SELECT 
    s.name,
    (COUNT(CASE WHEN da.is_present = 1 THEN 1 END) / COUNT(*)) * 100 as attendance_rate
FROM students s
LEFT JOIN daily_attendance da ON s.student_id = da.student_id
GROUP BY s.student_id
HAVING attendance_rate < 75;
```

---

## 11. Database Security (Future Enhancement)

- User authentication and authorization
- Role-based access control (Admin, Manager, Student)
- SQL injection prevention through parameterized queries
- Data encryption for sensitive information

---

## 12. Conclusion

- This database design demonstrates:
- Proper normalization (1NF, 2NF, 3NF)  
- Relational integrity through foreign keys  
- Efficient data retrieval through indexes  
- Complete CRUD operation support  
- Advanced SQL query capabilities  
- Seamless Python integration for ML pipeline 

This schema provides a robust foundation for an AI-driven hostel meal demand forecasting system, ensuring accurate predictions, reduced food wastage, and data-driven decision making.

**Database Course Concepts Covered:**
- ER Modeling
- Normalization
- SQL DDL (CREATE, ALTER)
- SQL DML (INSERT, UPDATE, DELETE, SELECT)
- Joins (INNER, LEFT)
- Aggregation (GROUP BY, HAVING)
- Subqueries
- Constraints
- Indexes
- Database-Application Integration

---

**Designed by:** [AR_Rahman_Iftekhar_Shovon]  
**Date:** February 2026  
**Course:** Database Management Systems & Software Development Project