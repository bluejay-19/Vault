import streamlit as st
import pandas as pd 
import datetime
from utils import load_css, render_sidebar, check_auth, get_supabase_client

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
    <div style="background: #E8920A; border-radius: 12px; padding: 1.5rem;">
        🦝"Go ahead, upload it. Let's see how bad the damage is this time around!"
    </div>
""", unsafe_allow_html=True)


# File uploader 
uploaded_file = st.file_uploader(
    "Upload statement",
    type=["csv", "xlsx"]
)

# Month selection 
# get the current month number (1-12)
current_month_idx = datetime.datetime.today().month - 1
month_list = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]

# set the index parameter to pre-select the current month 
selected_month = st.selectbox("Select a month ", month_list, index=current_month_idx)

# Year selection 
# get the current calender year 
current_year = datetime.datetime.now().year

# generate choices from 2000 up until the current year 
years = list(range(2000, current_year + 1)) 

# reverse the list so that the newest year is at the top 
selected_year = st.selectbox("Select Year", reversed(years))

# currency select option
currency = st.selectbox("Currency", ["$", "£", "€", "ZMW", "R", "AED"], index=0)

# Income this month 
income = st.number_input("Income this month", min_value=0, max_value=1_000_000, value=0, step=100)
# Budget this month 
budget = st.number_input("Budget this month", min_value=0, max_value=1_000_000, value=0, step=100)
# Savings this month 
savings = st.number_input("Net Savings", min_value=-1_000_000, max_value=1_000_000, value=0, step=100)


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

    # lowercase columns & handle accidental trailing spaces 
    df.columns = [col.lower().strip() for col in df.columns]

    # Validate the columns
    # Validate empty dataframe
    if df.empty: 
        st.error("Yo! what do you expect me to do with a blank file, want me to draw you a picture? ")
        st.stop()

    # Validate Date column 
    if 'date' not in df.columns:
        st.error("How do you expect to analyse your spending without knowing when you spent the money. Where are the dates buddy?")
        st.stop()

    # Validate categories
    required_cols = {'food', 'rent', 'transport', 'entertainment', 'other', 'subscriptions', 'groceries', 'medical'}

    # Categories present in this file 
    present_cols = [col for col in df.columns if col in required_cols]
    if len(present_cols) == 0: 
        st.error("Okay, so no categories, you couldnt do column names? really!")
        st.stop()

    # Build category_breakdown - present categories get real totals, missing ones get 0 
    category_breakdown = {}
    for cat in required_cols:
        if cat in present_cols:
            category_breakdown[cat] = df[cat].sum()
        else: 
            category_breakdown[cat] = 0 
        
    
    # Fill NaN rows with 0 
    df = df.fillna(0)

    # Data preview 
    st.dataframe(df.head(10))

    # Reference data 
    # category_cols = [col for col in df.columns if col != 'Date']
    # category_breakdown = df[category_cols].sum().to_dict()    
    total_spent = df[present_cols].sum().sum()
    biggest_category = df[present_cols].sum().idxmax()

    st.write(category_breakdown)

    st.markdown(f""" 
        <div style="background: #E8920A ; border-radius: 12px; padding: 1.5rem;">
                🦝 <strong>Frank's Take</strong><br><br>
                "Well, okay wow talk about a spender, look at your total {total_spent:.2f}.
                Yea? and on what heres where all that moolah went {biggest_category}, ive seen raccons do better!"
        </div>
    """, unsafe_allow_html=True)

    # Save button 
    submitted = st.button("Save to Vault")

    if submitted: 
        try: 
            supabase = get_supabase_client()
            access_token = st.session_state.user.access_token
            supabase.auth.set_session(access_token, st.session_state.user.refresh_token)
            # store the user's ID 
            user_id = st.session_state.user.user.id

            # check if this month/year already has an upload 
            existing = supabase.table("uploads").select("id").eq("user_id", user_id).eq("month", month_list.index(selected_month) + 1).eq("year", selected_year).execute()
            if existing.data:
                st.error(f"You already have an upload for {selected_month} {selected_year}. Delete it from Supabase first if you want to replace it.")
                st.stop()

            # key = column name, value = data variable in python code
            upload_dict = {
                "user_id": user_id,
                "month" : month_list.index(selected_month) + 1,
                "year" : selected_year,
                "income" : income,
                "budget" : budget,
                "net_savings" : savings, 
                "total_spent" : float(total_spent),
                "category_breakdown" : {k: float(v) for k, v in category_breakdown.items()},
                "currency" : currency             
                }
            
            # supabase insert 
            supabase.table("uploads").insert(upload_dict).execute()

            st.success("All data saved!")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

