# pages/dashboard.py
import streamlit as st
from streamlit_option_menu import option_menu
from utils.analytics import calculate_user_metrics
from interfaces.authentication import render_login_form
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
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
                "icon": {"font-size": "16px"},
                "nav-link": {"margin": "0", "font-size": "16px", "background-color": "#393939", "border": "1px solid #ffffff"},
                "nav-link-selected": {"background-color": "#eb4034", "font-weight": "600"},
            })

    progress_bar = st.progress(0)
    status_text = st.empty()

    if selected == "Log Workout":
        for percent_complete in range(101):
            progress_bar.progress(percent_complete)
            status_text.text(f"Loading Log Workout: {percent_complete}%")
        render_log_workout_form()
    elif selected == "Workout Data":
        for percent_complete in range(101):
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
            # Radio buttons for broad category selection
            broad_category = st.radio(
                "Choose Broad Category",
                options=list(broad_to_specific.keys()), 
                key="broad_category"
            )
            # Force session state to update immediately
            if broad_category != st.session_state.workout_selections['broad_category']:
                st.session_state.workout_selections = {
                    'broad_category': broad_category,
                    'muscle_group': None,  # No muscle group selected yet
                    'workout_name': None,  # No workout selected yet
                    'equipment': None      # No equipment selected yet
                }

        # Muscle group selection
        with innercols[2]:
            st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Muscle Group</p>", 
                    unsafe_allow_html=True)
            # Update available muscle groups based on selected broad category
            muscle_groups = get_muscles_for_category(st.session_state.workout_selections['broad_category']) if st.session_state.workout_selections['broad_category'] else []
            muscle_group = st.radio(
                "Choose Muscle Group", 
                options=muscle_groups, 
                key="muscle_group"
            )
            # Force session state to update immediately
            if muscle_group != st.session_state.workout_selections['muscle_group']:
                workouts = get_workouts_for_muscle(muscle_group)
                st.session_state.workout_selections.update({
                    'muscle_group': muscle_group,
                    'workout_name': None,  # Reset workout selection
                    'equipment': None      # Reset equipment selection
                })

    with cols[3]:
        # Workout selection
        innercols = st.columns((1, .1, 1))
        with innercols[0]:
            st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Workout</p>", 
                    unsafe_allow_html=True)
            # Update available workouts based on selected muscle group
            workouts = get_workouts_for_muscle(st.session_state.workout_selections['muscle_group']) if st.session_state.workout_selections['muscle_group'] else []
            workout = st.radio(
                "Choose Workout", 
                options=workouts, 
                key="workout_name"
            )
            # Force session state to update immediately
            if workout != st.session_state.workout_selections['workout_name']:
                st.session_state.workout_selections.update({
                    'workout_name': workout,
                    'equipment': None  # Reset equipment selection
                })

        # Equipment selection
        with innercols[2]:
            st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center;'>Equipment</p>", 
                    unsafe_allow_html=True)
            # Update available equipment based on selected workout
            equipments = get_available_equipment(st.session_state.workout_selections['workout_name']) if st.session_state.workout_selections['workout_name'] else []
            equipment = st.radio(
                "Choose Equipment", 
                options=equipments, 
                key="equipment"
            )
            # Force session state to update immediately
            if equipment != st.session_state.workout_selections['equipment']:
                st.session_state.workout_selections['equipment'] = equipment

    st.write("")

    cols = st.columns((1, 2, 1))
    with cols[1]:
        # Form fields for logging the workout
        st.write("<p style='color: #EB4034; border: solid 1px white; border-radius: 8px; text-align: center; padding-top: -10px;'>Log Workout</p>", unsafe_allow_html=True)
        st.write("<p style='text-align: center; font-style: italic;'>(For cardio exercises, enter time in minutes as reps)</p>", unsafe_allow_html=True)
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
                reps = col.number_input("Reps", min_value=1, max_value=180)

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
                st.success("Workout Logged!")



def render_workout_data(metrics, workout_df):

    scorecol = st.columns((.5, 3, .5))
    with scorecol[1]:
        st.write("<h4 style='color: #EB4034; text-align: center;'>Workout Analysis</h4>", unsafe_allow_html=True)
        # Use the pre-calculated strength scores from workout_df
        analysis_df = workout_df[['workoutname', 'strength_score', 'adjusted_weight']].copy()
        
        # Filter out workouts with a strength score of 0
        analysis_df = analysis_df[analysis_df['strength_score'] > 0]
        
        # Get the maximum strength score for each workout
        analysis_df = analysis_df.groupby('workoutname').agg(
            max_strength_score=('strength_score', 'max'),
            max_weight_lifted=('adjusted_weight', 'max')
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
                    format="%.3f"
                ),
            }
        )

    # Create columns for 2 cards below
    cols = st.columns((2, .1, 2))
    with cols[0]:
        muscle_group_counts = workout_df['muscle_group'].value_counts()
        fig = plot_muscle_group_bar_chart(muscle_group_counts)
        if fig:
            st.pyplot(fig)
    with cols[2]:
        fig = plot_workout_strength_scores(workout_df)
        if fig:
            st.pyplot(fig)
            

plt.rcParams['figure.facecolor'] = '#0E1118'
plt.rcParams['axes.facecolor'] = '#0E1118'
plt.rcParams['savefig.facecolor'] = '#0E1118'
plt.rcParams['savefig.edgecolor'] = '#0E1118'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

def plot_workout_strength_scores(workout_df):
    if workout_df.empty:
        st.write("")
        st.write("")
        st.write("")
        st.write("<h4 style='color: #EB4034; text-align: center;'>No Data Found</h4>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        return

    workout_df = workout_df[workout_df['strength_score'] > 0]
    workout_df['workoutname'] = pd.Categorical(
        workout_df['workoutname'],
        categories=workout_df.groupby('workoutname')['strength_score'].mean().sort_values(ascending=False).index
    )

    plt.figure(figsize=(7,4), facecolor='#0E1118', edgecolor='#0E1118')
    sns.stripplot(x='workoutname', y='strength_score', data=workout_df, color='#EB4034', jitter=True)
    plt.title('Strength Scores by Workout')
    plt.xlabel('\nWorkout Name')
    plt.ylabel('Strength Score\n')
    plt.xticks(rotation=0)

    ax = plt.gca()
    ax.set_facecolor('#0E1118')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')

    return plt.gcf()

def plot_muscle_group_bar_chart(muscle_group_counts):
    if muscle_group_counts.empty:
        st.write("")
        st.write("")
        st.write("")
        st.write("<h4 style='color: #EB4034; text-align: center;'>No Data Found</h4>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        return

    plt.figure(figsize=(7,4), facecolor='#0E1118', edgecolor='#0E1118')
    ax = muscle_group_counts.plot(kind='bar', color='#EB4034')

    ax.set_facecolor('#0E1118')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')

    plt.title('Workouts by Muscle Group')
    plt.xlabel('\nMuscle Group')
    plt.ylabel('Count\n')
    plt.xticks(rotation=0)

    return plt.gcf()