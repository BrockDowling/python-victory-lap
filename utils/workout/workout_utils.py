# utils/workout/workout_utils.py
from .workout_data import(
    workout_equipment,
    broad_to_specific, 
    workout_names_dict,)


# Get available equipment options for a given workout
def get_available_equipment(workout_name):
    return workout_equipment.get(workout_name, ["None"])


# Get available workouts for a given muscle group
def get_workouts_for_muscle(muscle_group):
    return workout_names_dict.get(muscle_group, [])


# Get available muscle groups for a broad category
def get_muscles_for_category(broad_category):
    return broad_to_specific.get(broad_category, [])


# Initialize default workout selections
def initialize_workout_selections():
    first_category = "Upper Body"
    first_muscle = broad_to_specific[first_category][0]
    first_workout = workout_names_dict[first_muscle][0]
    first_equipment = workout_equipment.get(first_workout, ["None"])[0]
    
    return {
        'broad_category': first_category,
        'muscle_group': first_muscle,
        'workout_name': first_workout,
        'equipment': first_equipment
    }


