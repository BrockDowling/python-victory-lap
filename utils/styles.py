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
                position: sticky !important;
                top: 0 !important;
                z-index: 999 !important;
            }

            .stForm.st-emotion-cache-qcpnpn {
                border-color: transparent;
            }
            
             /* Reduce spacing between input elements */
            .stForm div {
                margin-top: 0 !important;
                margin-bottom: 0 !important;
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

            .stColumn.st-emotion-cache-1r6slb0 {
                padding: 10px !important;
                background-color: #0E1118 !important;
                border-radius: 10px !important;
                box-shadow: 0 0 14px 2px #333 !important;
                bottom: 20px !important;
                z-index: 100 !important;
            }
        </style>
        """, unsafe_allow_html=True
    )
