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

            div[data-testid=toastContainer] {
                align-items: center;
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

            .stColumn.st-emotion-cache-1we84oy {
                padding: 10px !important;
                margin-top: 10px;
                background-color: #0E1118 !important;
                border-radius: 10px !important;
                border: 1px solid rgba(235, 64, 52, 0.4);
                box-shadow: rgba(235, 64, 52, 0.4) 0px 5px, rgba(235, 64, 52, 0.3) 0px 10px, rgba(235, 64, 52, 0.2) 0px 15px, rgba(235, 64, 52, 0.1) 0px 20px, rgba(235, 64, 52, 0.05) 0px 25px, rgba(235, 64, 52, 0.4) 0px -5px, rgba(235, 64, 52, 0.3) 0px -10px, rgba(235, 64, 52, 0.2) 0px -15px, rgba(235, 64, 52, 0.1) 0px -20px, rgba(235, 64, 52, 0.05) 0px -25px;
                z-index: 100 !important;
            }

            .st-emotion-cache-0.elp1w7k0 {
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )
