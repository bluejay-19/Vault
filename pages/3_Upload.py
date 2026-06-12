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

st.markdown(""" 
    <div style="background: #F59E0B; border-radius: 12px; padding: 1.5rem;">
        🦝"Go ahead, upload it. Let's see how bad the damage is this time around!"
    </div>
""", unsafe_allow_html=True)


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
    
    # Validate empty dataframe
    if df.empty: 
        st.error("Yo! what do you expect me to do with a blank file, want me to draw you a picture? ")
        st.stop()

    # Validate Date column 
    if 'Date' not in df.columns:
        st.error("How do you expect to analyse your spending without knowing when you spent the money. Where are the dates buddy?")
        st.stop()

    # Validate categories
    required_cols = {'Food', 'Rent', 'Transport', 'Entertainment', 'Other', 'Subscriptions', 'Groceries', 'Medical'}
    if df.columns.isin(required_cols).any():
        st.write("okay cool nice categories")
    else: 
        st.error("Okay, so no categories, you couldnt do column names? really!")
        st.stop()
    
    # Fill NaN rows with 0 
    df = df.fillna(0)

    # Data preview 
    st.dataframe(df.head(10))

    # Reference data 
    category_cols = [col for col in df.columns if col != 'Date']
    total_spent = df[category_cols].sum().sum()
    biggest_category = df[category_cols].sum().idxmax()

    st.markdown(f""" 
        <div style="background: #F59E0B; border-radius: 12px; padding: 1.5rem;">
                🦝 <strong>Frank's Take</strong><br><br>
                "Well, okay wow talk about a spender, look at your total {total_spent:.2f}.
                Yea? and on what heres where all that moolah went {biggest_category}, ive seen raccons do better!"
        </div>
    """, unsafe_allow_html=True)