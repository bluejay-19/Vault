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

