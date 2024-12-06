# utils/analytics_utils.py
import pandas as pd
from datetime import datetime
from utils.db import format_workout_data, format_class_data

# Calculate all user metrics from workout and class data
def calculate_user_metrics(workout_data, class_data):

    # Format raw data
    workout_df = format_workout_data(workout_data)
    class_df = format_class_data(class_data)
    
    # Calculate metrics
    metrics = {
        'total_workouts': len(workout_df),
        'weight_lifted': workout_df['weightused'].sum() if not workout_df.empty else 0,
        'avg_weight': workout_df['weightused'].mean() if not workout_df.empty else 0.0,
        'streak': calculate_streak(class_df),
        'total_classes': len(class_df),
        'attendance_rate': calculate_attendance_rate(class_df)
    }
    
    return metrics, workout_df, class_df


def calculate_streak(class_df: pd.DataFrame) -> int:
    # Existing calculate_streak function
    if class_df.empty:
        return 0
    class_df['dateattended'] = pd.to_datetime(class_df['dateattended'])
    class_df = class_df.sort_values('dateattended')
    class_df['date_diff'] = (class_df['dateattended'] - class_df['dateattended'].shift(1)).dt.days
    streak = 1
    max_streak = 1
    for diff in class_df['date_diff']:
        if diff == 1:
            streak += 1
            if streak > max_streak:
                max_streak = streak
        else:
            streak = 1
    return max_streak


def calculate_attendance_rate(class_df: pd.DataFrame) -> float:
    # Existing calculate_attendance_rate function
    if class_df.empty:
        return 0.0
    total_possible_classes = 7
    attended_classes = len(class_df)
    return (attended_classes / total_possible_classes) * 100 if total_possible_classes != 0 else 0.0