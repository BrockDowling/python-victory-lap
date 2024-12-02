import streamlit as st

def inject_custom_styles():
    st.markdown(
        """
        <style>
            /* Main Application Container */
            .stApp {
                background: #0E1118;
                font-family: 'Helvetica Neue', sans-serif;
            }

            .block-container {
                padding-bottom: 10px !important;
                padding-top: 10px !important;
            }

            /* Hide Default Streamlit Components */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

            /* Alert Styling */
            .stAlertContainer {
                padding-bottom: 0;
                text-align: center;
                
            }

            /* Form Styling */
            .stForm {
                padding: 10px !important; /* Reduce form padding */
                margin-bottom: -100px !important; /* Reduce spacing below the form */
                background-color: #0E1118 !important; /* Match the form with the app's dark theme */
                border-radius: 10px !important; /* Rounded corners */
                box-shadow: 0 0 14px 0 #333 !important;
            }

            .stForm div {
                margin-bottom: 0 !important; /* Reduce spacing between input elements */
            }

            /* Number Input Styling */
            .stNumberInput {
                margin-bottom: 5px !important; /* Reduce space below number inputs */
            }

            /* Submit Button Styling */
            .stButton > button {
                width: 100%;
                background-color: #EB4034 !important;
                color: white !important;
                border: none !important;
                padding: 8px 16px !important; /* Adjust padding for smaller button size */
                border-radius: 4px !important;
                font-weight: 500 !important;
                transition: background-color 0.3s !important;
            }

            .stButton > button:hover {
                background-color: #cc3629 !important;
            }

            /* General Styling for Containers */
            .section-box {
                border: 2px solid #000;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            }

        </style>
        """, unsafe_allow_html=True
    )
