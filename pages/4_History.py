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

if not uploads:
    st.info("No history yet. Upload your first month to get started.")
else:
    currency = uploads[0]["currency"] if uploads[0].get("currency") else "$"

    # Top summary cards
    total_spent_all = sum(u["total_spent"] for u in uploads)
    avg_monthly_savings = sum(u["net_savings"] for u in uploads) / len(uploads)

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown(f"<p style='color:#A0AEC0; font-size:13px; margin-bottom:4px;'>Total Spent (All Months)</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color:#FFFFFF; margin:0;'>{currency}{total_spent_all:,.2f}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#A0AEC0; font-size:12px;'>Across {len(uploads)} month(s)</p>", unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.markdown(f"<p style='color:#A0AEC0; font-size:13px; margin-bottom:4px;'>Average Monthly Savings</p>", unsafe_allow_html=True)
            color = "#00B37D" if avg_monthly_savings >= 0 else "#EF4444"
            sign = "+" if avg_monthly_savings >= 0 else ""
            st.markdown(f"<h2 style='color:{color}; margin:0;'>{sign}{currency}{avg_monthly_savings:,.2f}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#A0AEC0; font-size:12px;'>Per month average</p>", unsafe_allow_html=True)
