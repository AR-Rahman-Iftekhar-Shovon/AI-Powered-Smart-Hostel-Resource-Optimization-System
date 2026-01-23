## Database Schema

**AI-Driven Smart Hostel Resource Optimization System**

## Overview

This database schema is designed to support an AI-driven system that predicts daily hostel meal demand using historical attendance data.
The schema focuses on data integrity, explainability, and ML readiness, rather than simple CRUD operations.

1. students

Purpose:
Stores basic information about hostel residents.
This table ensures relational integrity and enables future analytical expansion.

Fields:

- student_id INT PRIMARY KEY AUTO_INCREMENT

- name VARCHAR(100) NULL

- room_no VARCHAR(20) NULL

- department VARCHAR(50) NULL

- join_date DATE NULL



2. daily_attendance

Purpose:
Stores per-student, per-meal attendance records.
This is the primary data source for machine learning training and analysis.

Fields:

- attendance_id BIGINT PRIMARY KEY AUTO_INCREMENT

- student_id INT NOT NULL

- date DATE NOT NULL

- meal_type ENUM('Breakfast', 'Lunch', 'Dinner') NOT NULL

- is_present TINYINT(1) DEFAULT 1

- recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP

Constraints:

- UNIQUE (student_id, date, meal_type)

- FOREIGN KEY (student_id) REFERENCES students(student_id)

3. daily_meal_summary

Purpose:
Stores aggregated daily meal data along with AI predictions and final decision outputs.
Acts as the decision and audit layer of the system.

Fields:

- summary_id BIGINT PRIMARY KEY AUTO_INCREMENT

- date DATE NOT NULL

- meal_type ENUM('Breakfast', 'Lunch', 'Dinner') NOT NULL

- total_present INT NOT NULL

- food_prepared_kg DECIMAL(8,2) NULL

- food_consumed_kg DECIMAL(8,2) NULL

- wastage_kg DECIMAL(8,2) NULL

- predicted_students INT NULL

- prediction_model VARCHAR(50) NULL

- confidence_score DECIMAL(5,4) NULL

- decision_quantity DECIMAL(8,2) NULL

- created_at DATETIME DEFAULT CURRENT_TIMESTAMP

Constraints:

- UNIQUE (date, meal_type)

4. special_events

Purpose:
Stores contextual factors such as exams, holidays, or special events that influence attendance.
Used as feature input for machine learning models.

Fields:

- event_id INT PRIMARY KEY AUTO_INCREMENT

- event_date DATE NOT NULL

- event_name VARCHAR(100) NOT NULL

- impact_factor DECIMAL(3,2) DEFAULT 1.00

- description TEXT NULL

## Relationships Summary:

- students → daily_attendance (One-to-Many)

- daily_attendance → daily_meal_summary (Aggregated analytics)

- special_events → Used as contextual ML features

## Design Principles:

- Normalized relational structure

- Historical data preservation

- Explainable AI predictions

- Auditable decision records

- Future-ready and extensible

## Conclusion

This schema provides a robust foundation for an AI-driven hostel meal demand forecasting system, ensuring accurate predictions, reduced food wastage, and data-driven decision making.