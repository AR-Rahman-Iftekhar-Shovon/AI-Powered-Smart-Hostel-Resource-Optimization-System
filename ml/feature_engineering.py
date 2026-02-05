import os
import pandas as pd

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
data_path = os.path.join(project_root, 'data', 'attendance_summary.csv')

print("="*60)
print("FEATURE ENGINEERING")
print("="*60)

# Load data
print(f"\n📂 Loading data from: {data_path}")
df = pd.read_csv(data_path)
print(f"✅ Loaded {len(df)} records")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

print("\n🔧 Creating new features...")

# Time-based features
df['day_of_week_num'] = df['date'].dt.dayofweek   # 0=Monday, 6=Sunday
df['is_weekend'] = df['day_of_week_num'].apply(lambda x: 1 if x >= 5 else 0)
df['month'] = df['date'].dt.month                  # 1-12
df['day_of_month'] = df['date'].dt.day             # 1-31
df['is_month_start'] = df['day_of_month'].apply(lambda x: 1 if x <= 5 else 0)
df['is_month_end'] = df['day_of_month'].apply(lambda x: 1 if x >= 25 else 0)

# Meal type encoding (convert text to numbers)
meal_mapping = {
    'Breakfast': 0,
    'Lunch': 1,
    'Dinner': 2
}
df['meal_type_encoded'] = df['meal_type'].map(meal_mapping)

# Display created features
print("\n✅ Features created:")
new_features = [
    'day_of_week_num', 
    'is_weekend', 
    'month', 
    'day_of_month',
    'is_month_start',
    'is_month_end',
    'meal_type_encoded'
]
for feature in new_features:
    print(f"   • {feature}")

# Show sample with new features
print("\n📊 Sample data with new features:")
print(df[['date', 'meal_type', 'actual_attended'] + new_features].head(10))

# Save feature-ready dataset
output_path = os.path.join(project_root, 'data', 'attendance_features.csv')
df.to_csv(output_path, index=False)

print(f"\n💾 Saved to: {output_path}")
print(f"✅ Total columns: {len(df.columns)}")
print(f"✅ Total records: {len(df)}")
print("\n" + "="*60)
print("             Feature engineering complete!")
print("="*60)