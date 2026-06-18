import streamlit as st
import os
from utils import load_css, render_sidebar, check_auth, get_supabase_client
from groq import Groq

st.set_page_config(
    page_title="Vault — History",
    page_icon="🔒",
    layout="wide",
)

load_css()
check_auth()
render_sidebar(active_page="history")

st.markdown("## History")
st.markdown("<p style='color: #A0AEC0;'>Your spending archive — all the evidence, none of the excuses.</p>", unsafe_allow_html=True)

# Supabase fetch
supabase = get_supabase_client()
access_token = st.session_state.user.access_token
supabase.auth.set_session(access_token, st.session_state.user.refresh_token)
user_id = st.session_state.user.user.id

response = supabase.table("uploads").select("*").eq("user_id", user_id).order("year", desc=True).order("month", desc=True).execute()
uploads = response.data
