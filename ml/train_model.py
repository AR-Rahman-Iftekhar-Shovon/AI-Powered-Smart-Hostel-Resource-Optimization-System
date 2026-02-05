import os
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
train_path = os.path.join(project_root, 'data', 'train_data.csv')
test_path = os.path.join(project_root, 'data', 'test_data.csv')

print("="*60)
print("ML MODEL TRAINING - LINEAR REGRESSION")
print("="*60)

# Load training data
print(f"\nLoading training data from: {train_path}")
train_df = pd.read_csv(train_path)
print(f"Loaded {len(train_df)} training records")

# Load testing data
print(f"\nLoading testing data from: {test_path}")
test_df = pd.read_csv(test_path)
print(f"Loaded {len(test_df)} testing records")

# Define features and target
feature_columns = [
    'day_of_week_num',
    'is_weekend',
    'month',
    'day_of_month',
    'meal_type_encoded'
]
target_column = 'actual_attended'

# Prepare training data
X_train = train_df[feature_columns]
y_train = train_df[target_column]

# Prepare testing data
X_test = test_df[feature_columns]
y_test = test_df[target_column]

print("\n" + "="*60)
print("MODEL TRAINING")
print("="*60)

# Create and train Linear Regression model
print("\nCreating Linear Regression model...")
model = LinearRegression()

print("Training model...")
model.fit(X_train, y_train)

print("Model training complete!")

# Display model coefficients
print("\nModel Coefficients (Feature Importance):")
for feature, coef in zip(feature_columns, model.coef_):
    print(f"   {feature}: {coef:.4f}")
print(f"\n   Intercept: {model.intercept_:.4f}")

# Make predictions on training data
print("\n" + "="*60)
print("TRAINING SET PERFORMANCE")
print("="*60)

y_train_pred = model.predict(X_train)

train_mae = mean_absolute_error(y_train, y_train_pred)
train_mse = mean_squared_error(y_train, y_train_pred)
train_rmse = np.sqrt(train_mse)
train_r2 = r2_score(y_train, y_train_pred)

print(f"\nMean Absolute Error (MAE): {train_mae:.2f} students")
print(f"Root Mean Squared Error (RMSE): {train_rmse:.2f} students")
print(f"R² Score: {train_r2:.4f}")

# Make predictions on testing data
print("\n" + "="*60)
print("TESTING SET PERFORMANCE")
print("="*60)

y_test_pred = model.predict(X_test)

test_mae = mean_absolute_error(y_test, y_test_pred)
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)
test_r2 = r2_score(y_test, y_test_pred)

print(f"\nMean Absolute Error (MAE): {test_mae:.2f} students")
print(f"Root Mean Squared Error (RMSE): {test_rmse:.2f} students")
print(f"R² Score: {test_r2:.4f}")

# Show sample predictions vs actual
print("\n" + "="*60)
print("SAMPLE PREDICTIONS (First 10 from test set)")
print("="*60)

comparison_df = pd.DataFrame({
    'Actual': y_test.values[:10],
    'Predicted': y_test_pred[:10].round(0),
    'Error': (y_test.values[:10] - y_test_pred[:10]).round(2)
})
print(comparison_df)

# Save the trained model
model_path = os.path.join(project_root, 'ml', 'trained_model.pkl')
with open(model_path, 'wb') as file:
    pickle.dump(model, file)

print(f"\nModel saved to: {model_path}")

print("\n" + "="*60)
print("MODEL TRAINING COMPLETE!")
print("="*60)
print("\nModel Performance Summary:")
print(f"   • Training MAE: {train_mae:.2f}")
print(f"   • Testing MAE: {test_mae:.2f}")
print(f"   • Model can predict attendance with ±{test_mae:.0f} students error")
print("="*60)