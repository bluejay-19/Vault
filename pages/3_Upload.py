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

if uploaded_file is not None: 
    try: 
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            st.write("File looks good enough")
        else: 
            df = pd.read_excel(uploaded_file)
            st.write("File looks good enough")
    except: 
        st.error("So, whatever you just added did not work, I cannot read it, how about making it something I can read.")
        st.stop()

    # Validate the columns
    
    # Is df empty?
    if df.empty: 
        st.error("Yo! what do you expect me to do with a blank file, want me to draw you a picture? ")
        st.stop()

    # Does Date column exist 
    if 'Date' not in df.columns:
        st.error("How do you expect to analyse your spending without knowing when you spent the money. Where are the dates buddy?")
        st.stop()

    # Do at least one of the following exist: food, rent, transport, entertainment, other exist 
    required_cols = {'Food', 'Rent', 'Transport', 'Entertainment', 'Other', 'Subscriptions', 'Groceries', 'Medical'}
    if df.columns.isin(required_cols).any():
        st.write("okay cool nice categories")
    else: 
        st.error("Okay, so no categories, you couldnt do column names? really!")
        st.stop()
    
