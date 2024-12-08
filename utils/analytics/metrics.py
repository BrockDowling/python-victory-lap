# utils/analytics_utils.py
import pandas as pd
from utils.db import format_workout_data

def calculate_user_metrics(workout_data, user_weight):
    # Format raw data
    workout_df = format_workout_data(workout_data)
    
    # Filter out rows where weightused is less than 1 (to not calculate strength score for them)
    workout_df = workout_df[workout_df['weightused'] >= 1]

    # Calculate strength scores if we have user weight and valid workout data
    if user_weight and not workout_df.empty:
        workout_df['strength_score'] = (
            (workout_df['weightused'] * workout_df['repschosen'] * workout_df['setschosen']) / user_weight).round(3)
    else:
        workout_df['strength_score'] = 0
    
    # Calculate metrics
    metrics = {
        'total_workouts': len(workout_df),
        'weight_lifted': workout_df['weightused'].sum() if not workout_df.empty else 0,
        'avg_weight': workout_df['weightused'].mean() if not workout_df.empty else 0.0,
        'max_strength_score': workout_df['strength_score'].max() if not workout_df.empty else 0.0
    }
    
    return metrics, workout_df
