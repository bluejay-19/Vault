import streamlit as st
import pandas as pd 
from utils import load_css, render_sidebar, check_auth

st.set_page_config(
    page_title="Vault — Upload",
    page_icon="🔒",
    layout="wide",
)

load_css()
check_auth()
render_sidebar(active_page="upload")

st.markdown("## Upload Statements")
st.markdown("<p style='color: #A0AEC0;'>CSV or Excel files. Frank will do the rest.</p>", unsafe_allow_html=True)

# File uploader 
uploaded_file = st.file_uploader(
    "Upload statement",
    type=["csv", "xlsx"]
)

# Income this month 
income = st.number_input("Income this month", min_value=0, value=0, step=100)
# Budget this month 
budget = st.number_input("Budget this month", min_value=0, value=0, step=100)
# Savings this month 
savings = st.number_input("Net Savings", value=0, step=100)

# Parsing the uploaded file
