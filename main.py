# main.py
import streamlit as st
from utils.styles import inject_custom_styles
from interfaces.authentication import render_auth_page
from interfaces.dashboard import render_dashboard


# Main application entry point. Configures the Streamlit page and manages authentication flow.
def main():
    st.set_page_config(
        page_title="VICTORY LAP",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom styling
    inject_custom_styles()
    
    # Initialize session states
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "userid" not in st.session_state:
        st.session_state.userid = None
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None
        
    # Handle authentication status
    if st.session_state.authentication_status == "success":
        st.session_state.authentication_status = None  # Reset the flag
        st.session_state.logged_in = True
        
    # Render appropriate view based on authentication state
    if not st.session_state.logged_in:
        render_auth_page()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()