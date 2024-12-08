import streamlit as st
import psycopg
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from utils.db import (
    check_user_exists,
    create_user,
    get_user_details,
)

# Load environment variables
load_dotenv()


# Connect to the DB
def get_db_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"))

def render_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected = option_menu(
            menu_title="VICTORY LAP",
            options=["Login", "Join"],
            icons=['person', 'person-plus'],
            default_index=0,
            orientation="horizontal",
            styles={
                "menu-title": {"font-size": "30px", "text-align": "center", "font-weight": "bold"},
                "menu-icon": {"color": "#0E1118", "font-size": "0px"},
                "container": {"padding": "2px", "width": "95%", "background-color": "#0E1118"},
                "icon": {"font-size": "20px"},
                "nav-link": {"margin": "0", "font-size": "15px", "background-color": "#393939", "border": "1px solid #ffffff"},
                "nav-link-selected": {"background-color": "#eb4034"},
            })
        
        # Initialize auth_tab if it doesn't exist
        if "auth_tab" not in st.session_state:
            st.session_state["auth_tab"] = "Login"

        # Update session state based on selection
        if selected == "Login":
            st.session_state["auth_tab"] = "Login"
            render_login_form()
        elif selected == "Join":
            st.session_state["auth_tab"] = "Join"
            render_signup_form()


def render_login_form():
    with st.container():
        with st.form(key='login_form', clear_on_submit=True):
            email = st.text_input("Email", key="login_email", placeholder="Email")
            
            password = st.text_input("Password", type="password", key="login_password", placeholder="Password")
            
            submitted = st.form_submit_button("Log In")
            if submitted:
                handle_login(email, password)


def render_signup_form():
    with st.form(key='signup_form'):

        firstname = st.text_input("First Name", placeholder="First name")
        lastname = st.text_input("Last Name", placeholder="Last name")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Create password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")

        cols = st.columns([1,1])
        with cols[0]:
            gender = st.radio("Gender", options=["M", "F"], key="gender_radio", horizontal=True)
        with cols[1]:
            weight = st.number_input("Weight (lbs)", min_value=0, max_value=500)
        submitted = st.form_submit_button("Sign Up")
        if submitted:
            handle_signup(firstname, lastname, email, password, confirm_password, gender, weight)


def handle_login(email, password):
    if check_user_exists(email, password):
        user_details = get_user_details(email)
        if user_details:
            update_session_state(user_details, email)
            st.session_state.authentication_status = "success"
            st.rerun()
        else:
            st.error("User details not found. Please try again.")
    else:
        st.error("Invalid email or password")


def handle_signup(firstname, lastname, email, password, confirm_password, gender, weight):
    # Validates all required fields
    if not all([firstname, lastname, email, password, confirm_password]):
        st.error("Please fill out all required fields")
        return
    
    if password != confirm_password:
        st.error("Passwords do not match")
        return
        
    # Check if weight is valid
    if not weight or weight <= 0:
        st.error("Please enter a valid weight")
        return

    try:
        # Check for existing email
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT email FROM \"User\" WHERE email = %s", (email,))
        taken_emails = cur.fetchall()
        
        if taken_emails:  # If there are any results, email exists
            st.error("This email is already taken!")
            return
            
        # If we get here, attempt to create the user
        create_user(firstname, lastname, email, password, gender, weight)
        st.success("Account created! Please log in.")
        
    except Exception as e:
        st.error(f"Signup error: {str(e)}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()


def update_session_state(user_details, email):
    st.session_state.update({
        'logged_in': True,
        'userid': user_details[0],
        'firstname': user_details[1],
        'lastname': user_details[2],
        'gender': user_details[3],
        'weight': user_details[4],
        'email': email
    })