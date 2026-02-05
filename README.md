# AI-Powered-Smart-Hostel-Resource-Optimization-System

An AI-powered, data-driven system designed uses **Machine Learning** to predict hostel/mess meal demand, reduce food wastage, and avoid shortages. By leveraging historical data and machine learning, the system ensures efficient resource management and optimized meal preparation.

---

## Problem Statement
- University hostels face significant challenges in meal planning due to unpredictable student attendance. This leads to:
- **Food Wastage:** Overestimation results in excess preparation
- **Food Shortage:** Underestimation causes student dissatisfaction
- **Budget Inefficiency:** Poor resource planning increases costs
- Manual adjustment of meal quantities is inefficient and error-prone.
- Historical data patterns are not utilized effectively for forecasting.
This system addresses these challenges by predicting next-day meal demand and providing rule-based decisions on how much food should be prepared.

---

## Solution

Our AI-powered system analyzes historical attendance patterns and predicts future meal demand, enabling mess managers to make data-driven decisions about food preparation quantities.

---

## Features

#       *Database Management*
- Historical data collection and storage in a MySQL database.
- Complete CRUD operations
- Advanced SQL queries (JOINs, subqueries, aggregations)
- Referential integrity with foreign keys

 #      *Data Analytics*
- Exploratory Data Analysis (EDA)
- Statistical analysis and pattern recognition
- Feature engineering for ML readiness
- Attendance trend visualization

#       *Machine Learning*
- Linear Regression model for demand forecasting
- Explainable AI predictions
- Model performance evaluation (MAE, RMSE, R²)
- Date and meal-type based predictions

#       *Complete Data Pipeline*
- Automated data collection from database
- Data preprocessing and cleaning
- Feature engineering
- Model training and evaluation
- Prediction generation and storage

---

## Tech Stack

- **Language:** Python
- **Database:** MySQL
- **Machine Learning:** scikit-learn (Linear Regression / Decision Tree)
- **Libraries:** pandas, numpy, scikit-learn, matplotlib, mysql-connector-python
- **Version Control:** Git + GitHub

---

## Project Structure-

smart-hostel/
│
├── core/                         # Core system modules
│   ├── db_connection.py          # MySQL database connection
│   ├── data_loader.py            # Data fetching from database
│   ├── crud_operations.py        # Create, Read, Update, Delete operations
│   └── advanced_queries.py       # Complex SQL queries
│
├── ml/                           # Machine Learning pipeline
│   ├── prepare_data.py           # Train-test split
│   ├── train_model.py            # Model training
│   ├── predict.py                # Future predictions
│   └── trained_model.pkl         # Saved ML model
│
├── analytics/                    # Data analysis
│   ├── attendance_eda.py         # Exploratory Data Analysis
│   └── feature_engineering.py    # Feature creation
│
├── data/                          # Datasets
│   ├── attendance_summary.csv     # Raw attendance data
│   ├── attendance_features.csv    # Engineered features
│   ├── train_data.csv             # Training dataset
│   └── test_data.csv              # Testing dataset
│
├── docs/                          # Documentation
│   └── database_design.md         # Database schema documentation
│
└── README.md                      # Project overview (this file)

---

## Installation

#   *Prerequisites*
- Python 3.8 or higher
- MySQL 8.0 or higher
- Git

#   *Step 1: Clone Repository*
```bash
git clone https://github.com/yourusername/smart-hostel.git
cd smart-hostel
```

#   *Step 2: Install Dependencies*
```bash
pip install mysql-connector-python pandas numpy scikit-learn matplotlib
```

#  *Step 3: Database Setup*
1. Open MySQL Workbench
2. Create database:
```sql
CREATE DATABASE smart_hostel_db;
USE smart_hostel_db;
```
3. Run table creation scripts (see `docs/database_design.md`)

#  *Step 4: Configure Database Connection*
Edit `core/db_connection.py`:
```python
connection = mysql.connector.connect(
    host='localhost',
    database='smart_hostel_db',
    user='your_username',      # Change this
    password='your_password'   # Change this
)
```

---

## Usage

#      *Load Data to Database*
```bash
python core/data_to_pandas.py
```

#     *Perform EDA*
```bash
python analytics/attendance_eda.py
```

#    *Feature Engineering*
```bash
python analytics/feature_engineering.py
```

#    *Prepare Training Data*
```bash
python ml/prepare_data.py
```

#    *Train ML Model*
```bash
python ml/train_model.py
```

#    *Make Predictions*
```bash
python ml/predict.py
```

#    *Test CRUD Operations*
```bash
python core/crud_operations.py
```

#    *Run Advanced Queries*
```bash
python core/advanced_queries.py
```

---

## Key Achievements

**Database Design:** Fully normalized schema with proper relationships  
**Data Science Pipeline:** Complete EDA → Feature Engineering → ML  
**Explainable AI:** Linear Regression model with interpretable coefficients  
**Production Ready:** Modular code structure for easy deployment  
**Industry Standards:** Follows best practices in software development  

---

## Database Concepts Demonstrated

- Entity-Relationship (ER) Modeling
- Normalization (1NF, 2NF, 3NF)
- Primary Keys & Foreign Keys
- UNIQUE & NOT NULL Constraints
- CRUD Operations (Create, Read, Update, Delete)
- SQL Joins (INNER, LEFT)
- Aggregate Functions (COUNT, AVG, SUM)
- GROUP BY & HAVING Clauses
- Subqueries & Nested Queries
- CASE Statements
- Database-Application Integration

---

## ML Concepts Demonstrated

- Supervised Learning (Regression)
- Train-Test Split
- Feature Engineering
- Model Training & Evaluation
- Performance Metrics (MAE, RMSE, R²)
- Model Persistence (pickle)
- Prediction Pipeline

---

## Team (Self-Project)
- Leader & Core Developer: **AR Rahman Iftekhar Shovon**

---

## Documentation

- [Database Design Documentation](docs/database_design.md)

---

##  Future Enhancements

- [ ] Flask web dashboard for real-time predictions
- [ ] Interactive charts and visualizations
- [ ] SMS/Email alerts for mess managers
- [ ] Mobile application
- [ ] Advanced ML models (Random Forest, XGBoost)
- [ ] Real-time attendance tracking via QR codes

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For questions or collaboration:
- **Email:** ar.rahmaniftekharshovon@gmail.com
- **GitHub:** [@AR-Rahman-Iftekhar-Shovon](https://github.com/AR-Rahman-Iftekhar-Shovon)

---

**If you found this project helpful, please give it a star!**