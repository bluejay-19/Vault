import streamlit as st
from utils import load_css, render_sidebar, check_auth, get_supabase_client

st.set_page_config(
    page_title="Vault — Dashboard",
    page_icon="🔒",
    layout="wide",
)

load_css()
check_auth()
render_sidebar(active_page="dashboard")

st.markdown("## Dashboard")
st.markdown("<p style='color: #A0AEC0;'>Your spending at a glance.</p>", unsafe_allow_html=True)

# Supabase fetch 
# get supabase client and set session 
supabase = get_supabase_client()
access_token = st.session_state.user.access_token
supabase.auth.set_session(access_token, st.session_state.user.refresh_token)

# get user id 
user_id = st.session_state.user.user.id

# fetch query 
response = supabase.table("uploads").select("*").eq("user_id", user_id).order("year", desc=True).order("month", desc=True).execute()

uploads = response.data 

if not uploads: 
    st.info("You have not uploaded anything, go to the uploads tab and upload a sheet for analysing.")

else: 
    latest = uploads[0] # most recent month (already ordered newesst first)

    # parse category_breakdown - it comes back from Supabase as a dict already 
    category_breakdown = latest["category_breakdown"]

    # Summary numbers 
    total_spent = latest["total_spent"]
    biggest_category = max(category_breakdown, key=category_breakdown.get)
    budget = latest["budget"]
    total_savings = sum([upload["net_savings"] for upload in uploads])
 
    if len(uploads) > 1 and uploads[1]["total_spent"] != 0:
        comparison = ((uploads[0]["total_spent"] - uploads[1]["total_spent"]) / uploads[1]["total_spent"]) * 100
    else: 
        comparison = None


    # Summary cards 
    col1, col2, col3, col4 = st.columns(4)

    with col1: 
        with st.container(border=True):
            st.metric("Total Spent", f"${total_spent:,.2f}")

    with col2: 
        with st.container(border=True):
            st.metric("Biggest Category", biggest_category)

    with col3: 
        with st.container(border=True):
            if comparison is None: 
                st.metric("vs Last Month", "No previous data")
            else: 
                st.metric("vs Last Month", f"{comparison:+.1f}%")

    with col4: 
        with st.container(border=True):
            st.metric("Net Savings to Date", f"${total_savings:,.2f}")

    # Donut Chart 

    # Line Chart 

    # Frank's roast 