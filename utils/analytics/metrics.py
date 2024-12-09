# utils/analytics_utils.py
import pandas as pd
import numpy as np
from utils.db import format_workout_data

def calculate_user_metrics(workout_data, user_weight):
    # Format raw data
    workout_df = format_workout_data(workout_data)
    

    # Create adjusted_weight column
    workout_df['adjusted_weight'] = workout_df['weightused'].astype(float)
    workout_df.loc[workout_df['adjusted_weight'] == 0, 'adjusted_weight'] = 0.97 * user_weight

    # Calculate strength scores
    workout_df['strength_score'] = (
        (workout_df['adjusted_weight'] * workout_df['repschosen'] * workout_df['setschosen']) / user_weight).round(3)
     
     # Calculate training volume
    workout_df['training_volume'] = workout_df['setschosen'] * workout_df['repschosen'] * workout_df['adjusted_weight']
    
    # Calculate metrics
    metrics = {
        'total_workouts': len(workout_df),
        'weight_lifted': workout_df[workout_df['adjusted_weight'] != 0.97 * user_weight]['weightused'].sum(),
        'avg_weight': workout_df[workout_df['adjusted_weight'] != 0.97 * user_weight]['weightused'].mean(),
        'max_strength_score': workout_df['strength_score'].max()
    }
    
    return metrics, workout_df
