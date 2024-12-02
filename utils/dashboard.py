import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
from utils.db_utils import (
    get_workout_questions,
    get_user_classes,
    get_muscle_groups,
    get_equipment_list,
    get_class_details,
    insert_workout_data
)
from utils.styles import inject_custom_styles


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
    "Mobility": ["Stretching"],
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
    "Stretching": ["None"]
}

# Dictionary to map muscle grouping to isolated muscles
broad_to_specific = {
    "Upper Body": ["Chest", "Back", "Shoulders", "Biceps", "Triceps"],
    "Lower Body": ["Quads", "Hamstrings", "Glutes", "Calves"],
    "Core": ["Core"],
    "Full Body": ["Full Body"],
    "Cardio": ["Cardio"]
}

# Function to format workout data
def format_workout_data(workout_data):
    if not workout_data:
        return pd.DataFrame(columns=['workoutname', 'muscleid', 'equipmentid', 'weightused', 'setschosen', 'repschosen', 'timelogged', 'muscle_group', 'equipment'])
    
    df = pd.DataFrame(workout_data, columns=['workoutname', 'muscleid', 'equipmentid', 'weightused', 'setschosen', 'repschosen', 'timelogged'])
    muscle_groups = {mg[0]: mg[1] for mg in get_muscle_groups()}
    equipment_list = {eq[0]: eq[1] for eq in get_equipment_list()}
    
    df['muscle_group'] = df['muscleid'].map(muscle_groups.get)
    df['equipment'] = df['equipmentid'].map(equipment_list.get)
    
    return df

# Function to format class data
def format_class_data(class_data):
    if not class_data:
        return pd.DataFrame(columns=['classid', 'dateattended', 'daysattended', 'classname'])
    
    df = pd.DataFrame(class_data, columns=['classid', 'dateattended', 'daysattended'])
    class_details = {cd[0]: cd[1] for cd in get_class_details()}
    df['classname'] = df['classid'].map(class_details.get)
    return df

# Function to calculate streak
def calculate_streak(class_df):
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

# Function to calculate attendance rate
def calculate_attendance_rate(class_df):
    if class_df.empty:
        return 0.0
    total_possible_classes = 10  # Replace with actual value
    attended_classes = len(class_df)
    return (attended_classes / total_possible_classes) * 100 if total_possible_classes != 0 else 0.0

# Load and process data
userid = st.session_state.get('userid')
workout_data = get_workout_questions(userid)
class_data = get_user_classes(userid)

# Format data
workout_df = format_workout_data(workout_data)
class_df = format_class_data(class_data)

# Calculate metrics
total_workouts = len(workout_df)
weight_lifted = workout_df['weightused'].sum()
avg_weight = workout_df['weightused'].mean() if not workout_df.empty else 0.0
streak = calculate_streak(class_df)
total_classes = len(class_df)
attendance_rate = calculate_attendance_rate(class_df)


def render_dashboard():
    inject_custom_styles()

    # Option Menu for navigation
    selected = option_menu(
        menu_title="", 
        options=["Log a Workout", "View Workout Data", "View Class Data"],
        icons=['pencil-square', 'activity', 'list'],
        default_index=0,
        orientation="vertically",
        styles={
            "menu-title": {"font-size": "25px", "text-align": "center", "font-weight": "bold"},
            "menu-icon": {"color": "#0E1118", "font-size": "20px"},
            "container": {"padding": "0", "width": "300px", "background-color": "#0E1118"},
            "icon": {"font-size": "20px"},
            "nav-link": {"margin": "2px", "font-size": "20px", "background-color": "#393939", "border": "1px solid #ffffff"},
            "nav-link-selected": {"background-color": "#eb4034"},
        })

    # Display content based on selected option
    if selected == "Log a Workout":
        render_log_workout_form()
    elif selected == "View Workout Data":
        render_workout_data()
    elif selected == "View Class Data":
        render_class_data()

def render_log_workout_form():
   

    # Initialize session state variables if they don't exist
    if 'broad_category' not in st.session_state:
        st.session_state.broad_category = "Upper Body"
    if 'muscle_group' not in st.session_state:
        st.session_state.muscle_group = broad_to_specific[st.session_state.broad_category][0]
    if 'workout_name' not in st.session_state:
        st.session_state.workout_name = workout_names_dict[st.session_state.muscle_group][0]
    if 'equipment' not in st.session_state:
        st.session_state.equipment = workout_equipment.get(st.session_state.workout_name, ["None"])[0]

    # Create columns for each section (Broad Category, Muscle Group, Workout, Equipment)
    cols = st.columns(4)  # 4 sections: Broad Category, Muscle Group, Workout, Equipment

    # Broad category selection
    with cols[0]:
        st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Broad Category</p>", unsafe_allow_html=True)
        for category in broad_to_specific.keys():
            checked = st.checkbox(f"{category}", key=f"broad_{category}",
                                value=st.session_state.broad_category == category)
            if checked and st.session_state.broad_category != category:
                st.session_state.broad_category = category
                st.session_state.muscle_group = broad_to_specific[category][0]
                st.session_state.workout_name = workout_names_dict[st.session_state.muscle_group][0]
                st.session_state.equipment = workout_equipment.get(st.session_state.workout_name, ["None"])[0]
                st.rerun()

    # Muscle group selection
    with cols[1]:
        st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Muscle Group</p>", unsafe_allow_html=True)
        muscle_groups = broad_to_specific.get(st.session_state.broad_category, [])
        for muscle in muscle_groups:
            checked = st.checkbox(f"{muscle}", key=f"muscle_{muscle}",
                                value=st.session_state.muscle_group == muscle)
            if checked and st.session_state.muscle_group != muscle:
                st.session_state.muscle_group = muscle
                st.session_state.workout_name = workout_names_dict[muscle][0]
                st.session_state.equipment = workout_equipment.get(st.session_state.workout_name, ["None"])[0]
                st.rerun()

    # Workout selection
    with cols[2]:
        st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Workout</p>", unsafe_allow_html=True)
        workouts = workout_names_dict.get(st.session_state.muscle_group, [])
        for workout in workouts:
            checked = st.checkbox(f"{workout}", key=f"workout_{workout}",
                                value=st.session_state.workout_name == workout)
            if checked and st.session_state.workout_name != workout:
                st.session_state.workout_name = workout
                st.session_state.equipment = workout_equipment.get(workout, ["None"])[0]
                st.rerun()

    # Equipment selection
    with cols[3]:
        st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Equipment</p>", unsafe_allow_html=True)
        equipments = workout_equipment.get(st.session_state.workout_name, ["None"])
        for equipment in equipments:
            checked = st.checkbox(f"{equipment}", key=f"equipment_{equipment}",
                                value=st.session_state.equipment == equipment)
            if checked and st.session_state.equipment != equipment:
                st.session_state.equipment = equipment
                st.rerun()

    # Form fields for logging the workout
    with st.form(key='workout_form'):
        weight_used = st.number_input(
            "Total Weight Used (lbs)",
            min_value=0,
            max_value=1000,
            disabled=st.session_state.equipment == "None"
        )
        sets = st.number_input("Sets", min_value=1, max_value=10)
        reps = st.number_input("Reps", min_value=1, max_value=20)
        time = st.number_input("Workout time (mins)", min_value=1, max_value=180)

        submitted = st.form_submit_button("Log Workout")
        if submitted:
            insert_workout_data(
                userid,
                st.session_state.workout_name,
                st.session_state.muscle_group,
                st.session_state.equipment,
                weight_used if st.session_state.equipment != "None" else 0,
                sets,
                reps,
                time
            )
            st.success("Workout logged successfully!")
            st.rerun()



def render_workout_data():
    st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="text-align: left; color: #EB4034; margin-bottom: 10px; font-size: 20px; font-weight: 600;">Workout Data</h3>
            <hr style="margin-top: 0; margin-bottom: 20px;">
            \nTotal Workouts: {total_workouts}
            \nAvg Weight Used: {avg_weight}
            \nTotal Weight Lifted: {weight_lifted}
            \nStrength Score:
        </div>
    """, unsafe_allow_html=True)

def render_class_data():
    st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="text-align: left; color: #EB4034; margin-bottom: 10px; font-size: 20px; font-weight: 600;">Class Data</h3>
            <hr style="margin-top: 0; margin-bottom: 20px;">
            \nTotal Classes: {total_classes}
            \nAttendance Rate: {attendance_rate}
            \nCurrent Streak: {streak}
        </div>
    """, unsafe_allow_html=True)