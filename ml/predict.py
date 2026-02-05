import os
import pandas as pd
import pickle
from datetime import datetime

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
model_path = os.path.join(project_root, 'ml', 'trained_model.pkl')

print("="*60)
print("    AI PREDICTION SYSTEM - HOSTEL ATTENDANCE FORECASTING")
print("="*60)

# Load trained model
print(f"\nLoading trained model from: {model_path}")
with open(model_path, 'rb') as file:
    model = pickle.load(file)
print("Model loaded successfully!")

# Function to create features from date and meal type
def create_features(date_str, meal_type):
    """
    Create feature vector from date and meal type
    """
    # Convert string to datetime
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Extract features
    day_of_week_num = date_obj.weekday()  # 0=Monday, 6=Sunday
    is_weekend = 1 if day_of_week_num >= 5 else 0
    month = date_obj.month
    day_of_month = date_obj.day
    
    # Meal type encoding
    meal_mapping = {
        'Breakfast': 0,
        'Lunch': 1,
        'Dinner': 2
    }
    meal_type_encoded = meal_mapping.get(meal_type, 1)  # Default to Lunch
    
    # Create feature dictionary
    features = {
        'day_of_week_num': day_of_week_num,
        'is_weekend': is_weekend,
        'month': month,
        'day_of_month': day_of_month,
        'meal_type_encoded': meal_type_encoded
    }
    
    return features, date_obj

# Function to make prediction
def predict_attendance(date_str, meal_type):
    """
    Predict attendance for given date and meal type
    """
    # Create features
    features, date_obj = create_features(date_str, meal_type)
    
    # Convert to DataFrame (model expects this format)
    feature_df = pd.DataFrame([features])
    
    # Make prediction
    prediction = model.predict(feature_df)[0]
    
    # Round to nearest integer
    prediction_rounded = round(prediction)
    
    return prediction_rounded, features, date_obj

# Interactive prediction
print("\n" + "="*60)
print("                    MAKE A PREDICTION")
print("="*60)

# Example 1: Predict for specific date
print("\n📅 Example Prediction 1:")
date1 = "2026-01-25"
meal1 = "Lunch"

pred1, feat1, date_obj1 = predict_attendance(date1, meal1)

print(f"\n   Date: {date1} ({date_obj1.strftime('%A')})")
print(f"   Meal Type: {meal1}")
print(f"   Day of Week: {date_obj1.strftime('%A')}")
print(f"   Weekend: {'Yes' if feat1['is_weekend'] else 'No'}")
print(f"\n                  PREDICTED ATTENDANCE: {pred1} students")

# Example 2: Weekend prediction
print("\n" + "-"*60)
print("\n📅 Example Prediction 2:")
date2 = "2026-01-26"
meal2 = "Dinner"

pred2, feat2, date_obj2 = predict_attendance(date2, meal2)

print(f"\n   Date: {date2} ({date_obj2.strftime('%A')})")
print(f"   Meal Type: {meal2}")
print(f"   Day of Week: {date_obj2.strftime('%A')}")
print(f"   Weekend: {'Yes' if feat2['is_weekend'] else 'No'}")
print(f"\n                 PREDICTED ATTENDANCE: {pred2} students")

# Batch prediction for next 7 days
print("\n" + "="*60)
print("             NEXT 7 DAYS FORECAST (Lunch)")
print("="*60)

from datetime import timedelta

start_date = datetime(2026, 1, 25)
predictions_list = []

for i in range(7):
    current_date = start_date + timedelta(days=i)
    date_str = current_date.strftime('%Y-%m-%d')
    
    pred, feat, date_obj = predict_attendance(date_str, 'Lunch')
    
    predictions_list.append({
        'Date': date_str,
        'Day': date_obj.strftime('%A'),
        'Weekend': 'Yes' if feat['is_weekend'] else 'No',
        'Predicted_Attendance': pred
    })

forecast_df = pd.DataFrame(predictions_list)
print("\n", forecast_df.to_string(index=False))

# Calculate recommended food quantity (assuming 0.25 kg per student)
print("\n" + "="*60)
print("         RESOURCE PLANNING RECOMMENDATION")
print("="*60)

avg_prediction = forecast_df['Predicted_Attendance'].mean()
food_per_student = 0.25  # kg per student
recommended_food = avg_prediction * food_per_student

print(f"\nAverage predicted attendance (next 7 days): {avg_prediction:.0f} students")
print(f"Recommended food preparation: {recommended_food:.2f} kg per meal")
print(f"Weekly food requirement (Lunch only): {recommended_food * 7:.2f} kg")

print("\n" + "="*60)
print("                 PREDICTION COMPLETE!")
print("="*60)