# utils/analytics_utils.py
import pandas as pd
import psycopg
import datetime 
from dotenv import load_dotenv
import os
from datetime import datetime as dt
from datetime import timedelta
from utils.db import format_workout_data, format_class_data

# load environment variable
load_dotenv()

def get_db_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"))

conn = get_db_connection()
cur = conn.cursor()

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
        'attendance_rate': calculate_attendance_rate(class_df),
        'lifetime Score': calc_lifetime_score(workout_df),
        'Weekly Score': calc_weekly_score(workout_df)
    }
    
    return metrics, workout_df, class_df


def calculate_streak(class_df: pd.DataFrame) -> int:
    # Your existing calculate_streak function
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
    # Your existing calculate_attendance_rate function
    if class_df.empty:
        return 0.0
    total_possible_classes = 7  # Replace with actual value
    attended_classes = len(class_df)
    return (attended_classes / total_possible_classes) * 100 if total_possible_classes != 0 else 0.0

def calc_lifetime_score(userid):
    try:
        cur.execute("SELECT SUM(workoutscore) from workoutquestions WHERE userid = %s", (userid,))
        LtScore = cur.fetchone()[0]
        return float(LtScore) if LtScore is not None else 0.0
    except Exception as e: 
        print(f"Error calculating lifetime score for user {userid}: {e}")
        return 0.0



def calc_weekly_score(workout_df: pd.DataFrame) -> float:
    current_day = datetime.date.today()
    start_date = current_day - datetime.timedelta(days = current_day.weekday() + 1)
    end_date = current_day + datetime.timedelta(days = 6)
    scores = workout_df.loc[start_date:end_date, 'workoutscore']
    return scores.sum()

 