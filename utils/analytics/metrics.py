# utils/analytics_utils.py
import pandas as pd
import numpy as np
from utils.db import format_workout_data

def calculate_user_metrics(workout_data, user_weight):
    # Format raw data
    workout_df = format_workout_data(workout_data)
    
    # Filter out rows where weightused is less than 1 (to not calculate strength score for them)
    workout_df = workout_df[workout_df['weightused'] >= 1]

    # Check if workout_df is empty
    # reduce call use of .empty(), call function that checks rather than command everytime
    is_empty = workout_df.empty

    # Calculate strength scores if we have user weight and valid workout data
    if user_weight and not is_empty:
        workout_df['strength_score'] = np.where(
            workout_df['weightused'] >=1,
            (workout_df['weightused'] * workout_df['repschosen'] * workout_df['setschosen']) /user_weight, 0
            ).round(3)
    # Calculate metrics
    metrics = {
        'total_workouts': len(workout_df),
        'weight_lifted': workout_df['weightused'].sum() if not is_empty else 0,
        'avg_weight': workout_df['weightused'].mean() if not is_empty else 0.0,
        'max_strength_score': workout_df['strength_score'].max() if not is_empty else 0.0
    }
    
    return metrics, workout_df
