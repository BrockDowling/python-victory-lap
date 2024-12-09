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
                padding-bottom: 5px;
                padding-top: 5px;
                text-align: center;
                position: sticky !important;
                top: 0 !important;
                z-index: 999 !important;
            }
            
            /* Progress bar styling */
            .stProgress > div > div > div > div {
                background-color: #EB4034;
            }
           
            div[data-testid=stToast] {
                background-color: #64bd6440;  
                width: 20%;
            }
             
            [data-testid=toastContainer] [data-testid=stMarkdownContainer] > p {
                font-size: 20px; font-style: normal; font-weight: 400;
                text-align: center;
                foreground-color: #ffffff;
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
            }

            /* Add new checkbox container styling */
            .stCheckbox {
                padding-top: 2px;
                padding-bottom: 0px;
            }

            .st-emotion-cache-0.elp1w7k0 {
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )
