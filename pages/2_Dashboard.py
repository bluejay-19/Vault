import streamlit as st
from utils import load_css, render_sidebar

st.set_page_config(
    page_title="Vault — Dashboard",
    page_icon="🔒",
    layout="wide",
)

load_css()
render_sidebar(active_page="dashboard")

st.markdown("## Dashboard")
st.markdown("<p style='color: #A0AEC0;'>Your spending at a glance.</p>", unsafe_allow_html=True)
st.info("🚧 Dashboard — coming Day 5")