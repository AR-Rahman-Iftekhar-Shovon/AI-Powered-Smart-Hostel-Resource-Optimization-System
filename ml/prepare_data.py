import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Use relative path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
data_path = os.path.join(project_root, 'data', 'attendance_features.csv')

print("="*60)
print("ML DATA PREPARATION - TRAIN-TEST SPLIT")
print("="*60)

# Load feature-engineered data
print(f"\nLoading data from: {data_path}")
df = pd.read_csv(data_path)

print(f"Loaded {len(df)} records")
print(f"\nColumns available: {list(df.columns)}")

# Define Features (X) and Target (y)
print("\n" + "="*60)
print("FEATURE SELECTION")
print("="*60)

# Features to use for ML model
feature_columns = [
    'day_of_week_num',
    'is_weekend',
    'month',
    'day_of_month',
    'meal_type_encoded'
]

# Check if all features exist
missing_features = [col for col in feature_columns if col not in df.columns]
if missing_features:
    print(f"Missing features: {missing_features}")
    print("Please run feature_engineering.py first!")
    exit()

# Target variable (what we want to predict)
target_column = 'actual_attended'

if target_column not in df.columns:
    print(f"Target column '{target_column}' not found!")
    exit()

# Separate Features and Target
X = df[feature_columns]
y = df[target_column]

print(f"\nFeatures (X): {feature_columns}")
print(f"Target (y): {target_column}")
print(f"\nX shape: {X.shape}")
print(f"y shape: {y.shape}")

# Train-Test Split (80% train, 20% test)
print("\n" + "="*60)
print("TRAIN-TEST SPLIT (80-20)")
print("="*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% for testing
    random_state=42,    # For reproducibility
    shuffle=True        # Shuffle data before splitting
)

print(f"\nTraining set: {len(X_train)} records ({len(X_train)/len(X)*100:.1f}%)")
print(f"Testing set:  {len(X_test)} records ({len(X_test)/len(X)*100:.1f}%)")

# Create train and test dataframes
train_df = pd.concat([X_train, y_train], axis=1)
test_df = pd.concat([X_test, y_test], axis=1)

# Save to CSV
train_path = os.path.join(project_root, 'data', 'train_data.csv')
test_path = os.path.join(project_root, 'data', 'test_data.csv')

train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)

print(f"\nSaved training data to: {train_path}")
print(f"Saved testing data to: {test_path}")

# Display sample data
print("\n" + "="*60)
print("SAMPLE TRAINING DATA")
print("="*60)
print(train_df.head())

print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)
print("\nTraining set statistics:")
print(train_df.describe())

print("\nData preparation complete!")
print("="*60)
print("Next Step: Train ML model using train_data.csv")
print("="*60)