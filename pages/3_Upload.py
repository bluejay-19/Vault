import streamlit as st
import pandas as pd 
import datetime
from utils import load_css, render_sidebar, check_auth, get_supabase_client

st.set_page_config(
    page_title="Vault — Upload",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
check_auth()
render_sidebar(active_page="upload")

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    .stButton > button * {
        color: #0F1117 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## Upload Statements")      
st.markdown("<p style='color: #A0AEC0;'>CSV or Excel files. Frank will do the rest.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Frank quote card
st.markdown(""" 
    <div style="background:#1A1D2E; border: 1px solid #E8920A; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; display:flex; align-items:center; gap:0.75rem;">
        <span style="font-size:1.5rem;">🦝</span>
        <span style="color:#E8920A; font-weight:500; font-size:1rem;">"Go ahead, upload it. Let's see how bad the damage is this time around!"</span>
    </div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Upload your monthly statement",
    type=["csv", "xlsx"]
)

st.markdown("<br>", unsafe_allow_html=True)

# Month, Year, Currency in one row
col_m, col_y, col_c = st.columns(3)

current_month_idx = datetime.datetime.today().month - 1
month_list = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
current_year = datetime.datetime.now().year
years = list(range(2000, current_year + 1))

with col_m:
    selected_month = st.selectbox("Month", month_list, index=current_month_idx)
with col_y:
    selected_year = st.selectbox("Year", reversed(years))
with col_c:
    currency = st.selectbox("Currency", ["$", "£", "€", "ZMW", "R", "AED"], index=0)

st.markdown("<br>", unsafe_allow_html=True)

# Income, Budget, Savings in one row
col_i, col_b, col_s = st.columns(3)

with col_i:
    income = st.number_input("Income this month", min_value=0, max_value=1_000_000, value=0, step=100)
with col_b:
    budget = st.number_input("Budget this month", min_value=0, max_value=1_000_000, value=0, step=100)
with col_s:
    savings = st.number_input("Net Savings", min_value=-1_000_000, max_value=1_000_000, value=0, step=100)

st.markdown("<br>", unsafe_allow_html=True)

# Parsing the uploaded file
if uploaded_file is not None: 
    try: 
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else: 
            df = pd.read_excel(uploaded_file)
    except: 
        st.error("So, whatever you just added did not work, I cannot read it, how about making it something I can read.")
        st.stop()

    df.columns = [col.lower().strip() for col in df.columns]

    if df.empty: 
        st.error("Yo! what do you expect me to do with a blank file, want me to draw you a picture?")
        st.stop()

    if 'date' not in df.columns:
        st.error("How do you expect to analyse your spending without knowing when you spent the money. Where are the dates buddy?")
        st.stop()

    required_cols = {'food', 'rent', 'transport', 'entertainment', 'other', 'subscriptions', 'groceries', 'medical'}
    present_cols = [col for col in df.columns if col in required_cols]

    if len(present_cols) == 0: 
        st.error("Okay, so no categories, you couldn't do column names? really!")
        st.stop()

    category_breakdown = {}
    for cat in required_cols:
        if cat in present_cols:
            category_breakdown[cat] = df[cat].sum()
        else: 
            category_breakdown[cat] = 0 

    df = df.fillna(0)

    total_spent = df[present_cols].sum().sum()
    biggest_category = df[present_cols].sum().idxmax()

    # Data preview
    with st.expander("Preview uploaded data"):
        st.dataframe(df.head(10))

    st.markdown(f""" 
        <div style="background:transparent; border: 1px solid #E8920A; border-radius: 12px; padding: 1.5rem;">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
                <span style="font-size:1.2rem;">🦝</span>
                <strong style="color:#1A0F00;">Frank's Take</strong>
            </div>
            <p style="color:#1A0F00; margin:0;">Total spending: {currency}{total_spent:,.2f} — biggest drain is <strong>{biggest_category}</strong>. Let's see if you can explain yourself.</p>
        </div>
    """, unsafe_allow_html=True)

    submitted = st.button("Save to Vault", use_container_width=True)

    if submitted: 
        try: 
            supabase = get_supabase_client()
            access_token = st.session_state.user.access_token
            supabase.auth.set_session(access_token, st.session_state.user.refresh_token)
            user_id = st.session_state.user.user.id

            existing = supabase.table("uploads").select("id").eq("user_id", user_id).eq("month", month_list.index(selected_month) + 1).eq("year", selected_year).execute()
            if existing.data:
                st.error(f"You already have an upload for {selected_month} {selected_year}. Delete it from Supabase first if you want to replace it.")
                st.stop()

            upload_dict = {
                "user_id": user_id,
                "month": month_list.index(selected_month) + 1,
                "year": selected_year,
                "income": income,
                "budget": budget,
                "net_savings": savings, 
                "total_spent": float(total_spent),
                "category_breakdown": {k: float(v) for k, v in category_breakdown.items()},
                "currency": currency             
            }
            
            supabase.table("uploads").insert(upload_dict).execute()
            st.success("All data saved! Head to the Dashboard to see Frank's full roast.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")