#utils/workout/workout_data.py

# Dictionary for the workout names
workout_names_dict = {
    "Chest": ["Bench Press", "Push Ups", "Pec Flies"],
    "Back": ["Lat pulls", "Rows"],
    "Shoulders": ["Shoulder Press"],
    "Biceps": ["Bicep Curls"],
    "Triceps": ["Tricep Extensions", "Dips"],
    "Quads": ["Squats", "Lunges", "Leg Press", "Box Jumps"],
    "Hamstrings": ["Deadlift", "Lunges"],
    "Glutes": ["Hip Thrusters"],
    "Calves": ["Calf Raises"],
    "Core": ["Crunches", "Planks"],
    "Full Body": ["Deadlift"],
    "Cardio": ["Running", "Cycling", "Jump Rope"]
}

# Dictionary mapping workouts to their allowed equipment
workout_equipment = {
    "Pec Flies": ["Dumbbells"],
    "Dips": ["None"],
    "Bench Press": ["Barbell", "Dumbbells"],
    "Push Ups": ["None"],
    "Bicep Curls": ["Dumbbells", "Barbell", "Cables"],
    "Tricep Extensions": ["Dumbbells", "Cables"],
    "Shoulder Press": ["Dumbbells", "Barbell"],
    "Lat pulls": ["Cables"],
    "Squats": ["Barbell", "Dumbbells"],
    "Lunges": ["Dumbbells", "None"],
    "Leg Press": ["Machine"],
    "Calf Raises": ["Dumbbells", "None"],
    "Deadlift": ["Barbell"],
    "Hip Thrusters": ["Barbell"],
    "Running": ["None"],
    "Cycling": ["None"],
    "Jump Rope": ["None"],
    "Planks": ["None"],
    "Rows": ["Machine", "Cables", "Barbell", "Dumbbells"],
    "Box Jumps": ["None"],
    "Crunches": ["None"],
}

# Dictionary to map muscle grouping to isolated muscles
broad_to_specific = {
    "Upper Body": ["Chest", "Back", "Shoulders", "Biceps", "Triceps"],
    "Lower Body": ["Quads", "Hamstrings", "Glutes", "Calves"],
    "Core": ["Core"],
    "Full Body": ["Full Body"],
    "Cardio": ["Cardio"]
}