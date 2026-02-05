import os
import pandas as pd

# Use relative path for cross-platform compatibility
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
data_path = os.path.join(project_root, 'data', 'attendance_summary.csv')

# Load attendance summary data
print("📂 Loading data from:", data_path)
df = pd.read_csv(data_path)

print("\n========== DATASET OVERVIEW ==========")
print(df.info())

print("\n========== SAMPLE RECORDS ==========")
print(df.head(10))

# Basic EDA metrics
total_records = len(df)
average_attendance = df['actual_attended'].mean()
max_attendance = df['actual_attended'].max()
min_attendance = df['actual_attended'].min()
std_attendance = df['actual_attended'].std()

print("\n========== KEY STATISTICS ==========")
print(f"📊 Total Records: {total_records}")
print(f"📈 Average Attendance: {average_attendance:.2f}")
print(f"🔼 Maximum Attendance: {max_attendance}")
print(f"🔽 Minimum Attendance: {min_attendance}")
print(f"📉 Standard Deviation: {std_attendance:.2f}")

# Meal-wise average attendance
print("\n========== MEAL-WISE AVERAGE ATTENDANCE ==========")
meal_avg = df.groupby('meal_type')['actual_attended'].mean()
print(meal_avg)

# Day-wise pattern (if day_of_week column exists)
if 'day_of_week' in df.columns:
    print("\n========== DAY-WISE AVERAGE ATTENDANCE ==========")
    day_avg = df.groupby('day_of_week')['actual_attended'].mean()
    print(day_avg)

# Weekend vs Weekday analysis (if is_weekend column exists)
if 'is_weekend' in df.columns:
    print("\n========== WEEKEND VS WEEKDAY ==========")
    weekend_avg = df.groupby('is_weekend')['actual_attended'].mean()
    print("Weekday Average:", weekend_avg.get(0, 'N/A'))
    print("Weekend Average:", weekend_avg.get(1, 'N/A'))

print("\n========== ATTENDANCE VARIABILITY ==========")

daily_stats = df.groupby('date')['actual_attended'].agg(['mean', 'std'])
print(daily_stats)

print("\nOverall Standard Deviation of Attendance:")
print(df['actual_attended'].std())

# After your existing code, add:

print("\n========== MISSING VALUES CHECK ==========")
missing_values = df.isnull().sum()
print(missing_values)
print(f"Total missing values: {missing_values.sum()}")

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== UNIQUE VALUES COUNT ==========")
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique values")

print("\n========== ATTENDANCE DISTRIBUTION ==========")
print(df['actual_attended'].describe())

print("\n========== MEAL TYPE DISTRIBUTION ==========")
print(df['meal_type'].value_counts())

# Check for outliers using IQR method
print("\n========== OUTLIER DETECTION (IQR Method) ==========")
Q1 = df['actual_attended'].quantile(0.25)
Q3 = df['actual_attended'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['actual_attended'] < lower_bound) | (df['actual_attended'] > upper_bound)]
print(f"Q1 (25th percentile): {Q1}")
print(f"Q3 (75th percentile): {Q3}")
print(f"IQR: {IQR}")
print(f"Lower Bound: {lower_bound}")
print(f"Upper Bound: {upper_bound}")
print(f"Number of outliers: {len(outliers)}")
if len(outliers) > 0:
    print("\nOutlier records:")
    print(outliers)

print("\n========== CORRELATION ANALYSIS ==========")
# If you have numeric columns like is_weekend, day_number, etc.
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
if len(numeric_cols) > 1:
    correlation = df[numeric_cols].corr()
    print(correlation)
else:
    print("Not enough numeric columns for correlation")

print("\nStatistical EDA Stage-1 Complete!")
print("=" * 60)
print("📌 Key Findings Summary:")
print(f"   • Dataset has {len(df)} records")
print(f"   • Average attendance: {df['actual_attended'].mean():.2f}")
print(f"   • Attendance varies by ±{df['actual_attended'].std():.2f}")
print(f"   • {len(outliers)} potential outlier(s) detected")
print("=" * 60)


print("\nEDA Complete!")