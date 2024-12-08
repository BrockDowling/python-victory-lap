# pages/dashboard.py
import streamlit as st
from streamlit_option_menu import option_menu
from utils.analytics import calculate_user_metrics
from interfaces.authentication import render_login_form
from utils.db import (
    get_workout_questions,
    insert_workout_data)
from utils.workout.workout_utils import (
    get_available_equipment,
    get_workouts_for_muscle,
    get_muscles_for_category,
    initialize_workout_selections,
    broad_to_specific)
from utils.styles import inject_custom_styles
import time

def render_dashboard():
    # Check if user is logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        # If not logged in, show the login form
        render_login_form()
        return
    # Load and process data
    userid = st.session_state.get('userid')
    user_weight = st.session_state.get('weight')
    workout_data = get_workout_questions(userid)
    
    # Calculate all metrics at once
    metrics, workout_df = calculate_user_metrics(workout_data, user_weight)

    inject_custom_styles()

    # Option Menu for navigation
    cols = st.columns((1, 2, 1))
    with cols[1]:
        selected = option_menu(
            menu_title="DASHBOARD", 
            options=["Log Workout", "Workout Data"],
            icons=['pencil-square', 'activity'],
            default_index=0,
            orientation="horizontal",
            styles={
                "menu-title": {"font-size": "30px", "text-align": "center", "font-weight": "bold"},
                "menu-icon": {"color": "#0E1118", "font-size": "0px"},
                "container": {"padding": "2px", "width": "95%", "background-color": "#0E1118"},
                "icon": {"font-size": "15px"},
                "nav-link": {"margin": "0", "font-size": "15px", "background-color": "#393939", "border": "1px solid #ffffff"},
                "nav-link-selected": {"background-color": "#eb4034"},
            })

    progress_bar = st.progress(0)
    status_text = st.empty()

    if selected == "Log Workout":
        for percent_complete in range(101):
            time.sleep(0.5)  # Simulate some processing time
            progress_bar.progress(percent_complete)
            status_text.text(f"Loading Log Workout: {percent_complete}%")
        render_log_workout_form()
    elif selected == "Workout Data":
        for percent_complete in range(101):
            time.sleep(0.5)  # Simulate some processing time
            progress_bar.progress(percent_complete)
            status_text.text(f"Loading Workout Data: {percent_complete}%")
        render_workout_data(metrics, workout_df)

    # Remove the progress bar and status text after loading
    progress_bar.empty()
    status_text.empty()

def render_log_workout_form():
    # Initialize session state variables if they don't exist
    if 'workout_selections' not in st.session_state:
        st.session_state.workout_selections = initialize_workout_selections()

    # Create columns for each section
    cols = st.columns((.1, 2.5, .1, 2.5, .1))


    with cols[1]:
        # Broad category selection
        innercols = st.columns((1, .1, 1))
        with innercols[0]:
            st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Broad Category</p>", 
                    unsafe_allow_html=True)
            for category in broad_to_specific.keys():
                checked = st.checkbox(
                    f"{category}", 
                    key=f"broad_{category}",
                    value=st.session_state.workout_selections['broad_category'] == category
                )
                if checked and st.session_state.workout_selections['broad_category'] != category:
                    st.session_state.workout_selections = {
                        'broad_category': category,
                        'muscle_group': get_muscles_for_category(category)[0],
                        'workout_name': get_workouts_for_muscle(get_muscles_for_category(category)[0])[0],
                        'equipment': get_available_equipment(get_workouts_for_muscle(get_muscles_for_category(category)[0])[0])[0]
                    }

        # Muscle group selection
        with innercols[2]:
            st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Muscle Group</p>", 
                    unsafe_allow_html=True)
            muscle_groups = get_muscles_for_category(st.session_state.workout_selections['broad_category'])
            for muscle in muscle_groups:
                checked = st.checkbox(
                    f"{muscle}", 
                    key=f"muscle_{muscle}",
                    value=st.session_state.workout_selections['muscle_group'] == muscle
                )
                if checked and st.session_state.workout_selections['muscle_group'] != muscle:
                    workouts = get_workouts_for_muscle(muscle)
                    st.session_state.workout_selections.update({
                        'muscle_group': muscle,
                        'workout_name': workouts[0],
                        'equipment': get_available_equipment(workouts[0])[0]
                    })

    with cols[3]:
        # Workout selection
        innercols = st.columns((1, .1, 1))
        with innercols[0]:
            st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Workout</p>", 
                    unsafe_allow_html=True)
            workouts = get_workouts_for_muscle(st.session_state.workout_selections['muscle_group'])
            for workout in workouts:
                checked = st.checkbox(
                    f"{workout}", 
                    key=f"workout_{workout}",
                    value=st.session_state.workout_selections['workout_name'] == workout
                )
                if checked and st.session_state.workout_selections['workout_name'] != workout:
                    st.session_state.workout_selections.update({
                        'workout_name': workout,
                        'equipment': get_available_equipment(workout)[0]
                    })


        # Equipment selection
        with innercols[2]:
            st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Equipment</p>", 
                    unsafe_allow_html=True)
            equipments = get_available_equipment(st.session_state.workout_selections['workout_name'])
            for equipment in equipments:
                checked = st.checkbox(
                    f"{equipment}", 
                    key=f"equipment_{equipment}",
                    value=st.session_state.workout_selections['equipment'] == equipment
                )
                if checked and st.session_state.workout_selections['equipment'] != equipment:
                    st.session_state.workout_selections['equipment'] = equipment

    st.write("")

    cols = st.columns((1, 2, 1))
    with cols[1]:
        # Form fields for logging the workout
        st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Log Workout</p>", 
            unsafe_allow_html=True)
        with st.form(key='workout_form'):
            row1 = st.columns(1)
            row2 = st.columns(1)
            row3 = st.columns(1)
            for col in row1:
                weight_used = col.number_input(
                    "Weight(lbs)",
                    min_value=0,
                    max_value=1000,
                    disabled=st.session_state.workout_selections['equipment'] == "None")
            for col in row2:
                sets = col.number_input("Sets", min_value=1, max_value=10)
            for col in row3:
                reps = col.number_input("Reps", min_value=1, max_value=20)

            submitted = st.form_submit_button("Log Workout")
            if submitted:
                response = insert_workout_data(
                    st.session_state.userid,
                    st.session_state.workout_selections['workout_name'],
                    st.session_state.workout_selections['muscle_group'],
                    st.session_state.workout_selections['equipment'],
                    weight_used if st.session_state.workout_selections['equipment'] != "None" else 0,
                    sets,
                    reps,)
                st.toast("Workout Logged!")


def render_workout_data(metrics, workout_df):
    # Create columns for metrics card
    cols = st.columns((1.5, .1, 1.5, .1, 1.5))

    if workout_df.empty:
        # Display "No data available" in all three cards
        with cols[2]:
            st.write("<h4 style='color: #EB4034; text-align: center;'>Workout Analysis</h4>", unsafe_allow_html=True)
            st.write("")
            st.write("<p style='color: #ffffff; text-align: center;'>No data available</p>", unsafe_allow_html=True)
            st.write("")
            st.write("")
        with cols[0]:
            st.write("<h4 style='color: #EB4034; text-align: center;'>Workouts by Muscle Group</h4>", unsafe_allow_html=True)
            st.write("")
            st.write("<p style='color: #ffffff; text-align: center;'>No data available</p>", unsafe_allow_html=True)
            st.write("")
            st.write("")
        with cols[4]:
            st.write("<h4 style='color: #EB4034; text-align: center;'>Max Weight by Exercise</h4>", unsafe_allow_html=True)
            st.write("")
            st.write("<p style='color: #ffffff; text-align: center;'>No data available</p>", unsafe_allow_html=True)
            st.write("")
            st.write("")
    else:
        with cols[2]:
            st.write("<h4 style='color: #EB4034; text-align: center;'>Workout Analysis</h4>", unsafe_allow_html=True)
            # Use the pre-calculated strength scores from workout_df
            analysis_df = workout_df[['workoutname', 'strength_score', 'weightused']].copy()
            
            # Filter out workouts with a strength score of 0
            analysis_df = analysis_df[analysis_df['strength_score'] > 0]
            
            # Get the maximum strength score for each workout
            analysis_df = analysis_df.groupby('workoutname').agg(
                max_strength_score=('strength_score', 'max'),
                max_weight_lifted=('weightused', 'max')
            ).reset_index()
            
            # Sort values by max_strength_score for clarity
            analysis_df = analysis_df.sort_values('max_strength_score', ascending=False)
            
            # Display the workout analysis dataframe
            st.dataframe(
                analysis_df[['workoutname', 'max_strength_score']],  # Only show relevant columns
                use_container_width=True,
                hide_index=True,
                column_config={
                    "workoutname": st.column_config.Column("Workout Name", width="small"),
                    "max_strength_score": st.column_config.NumberColumn(
                        "Max Strength Score",
                        help="Score = (Weight * Reps * Sets) / Body Weight",
                        format="%.3f"
                    ),
                }
            )
        
        with cols[0]:
            st.write("<h4 style='color: #EB4034; text-align: center;'>Workouts by Muscle Group</h4>", unsafe_allow_html=True)
            muscle_group_counts = workout_df['muscle_group'].value_counts()
            st.bar_chart(muscle_group_counts, color='#EB4034')

        with cols[4]:
            st.write("<h4 style='color: #EB4034; text-align: center;'>Max Weight by Exercise</h4>", unsafe_allow_html=True)
            max_weight_df = workout_df.groupby('workoutname').agg(max_weight_lifted=('weightused', 'max')).reset_index()
            max_weight_df = max_weight_df.sort_values('max_weight_lifted', ascending=False)
            st.bar_chart(max_weight_df.set_index('workoutname')['max_weight_lifted'], color='#EB4034')