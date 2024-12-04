import streamlit as st
from streamlit_option_menu import option_menu
from utils.db import (
    check_user_exists,
    create_user,
    get_user_details,
)


def render_auth_page():
    selected = option_menu(
    menu_title="VICTORY LAP   ",
    options=["Login", "Sign Up"],
    icons=['person', 'person-plus'],
    default_index=0,
    orientation="horizontal",
    styles={
        "menu-title": {"font-size": "30px", "font-weight": "bold"},
        "menu-icon": {"color": "#0E1118", "font-size": "0px"},
        "container": {"padding": "0", "width": "250px", "background-color": "#0E1118"},
        "icon": {"font-size": "20px"},
        "nav-link": {"margin": "0", "font-size": "15px", "background-color": "#393939", "border": "1px solid #ffffff"},
        "nav-link-selected": {"background-color": "#eb4034"},
    })

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if "auth_tab" not in st.session_state:
            st.session_state["auth_tab"] = "Login"

        if st.session_state["auth_tab"] in ["Login", "Sign Up"]:
            if selected == "Login":
                st.session_state["auth_tab"] = "Login"
                render_login_form()
            elif selected == "Sign Up":
                st.session_state["auth_tab"] = "Sign Up"
                render_signup_form()


def render_login_form():
    cols = st.columns([1])
    with cols[0]:
        with st.form(key='login_form'):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
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
            st.success("Successfully logged in!")
            st.rerun()
        else:
            st.error("User details not found. Please try again.")
    else:
        st.error("Invalid email or password")


def handle_signup(firstname, lastname, email, password, confirm_password, gender, weight):
    if not all([firstname, lastname, email, password, confirm_password]):
        st.error("Please fill out all required fields")
    elif password != confirm_password:
        st.error("Passwords do not match")
    else:
        try:
            create_user(firstname, lastname, email, password, gender, weight)
            st.success("Account created! Please log in.")
        except Exception as e:
            st.error(f"Signup error: {str(e)}")


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