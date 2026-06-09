import streamlit as st
from utils import load_css

st.set_page_config(
    page_title="Vault — Login",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

load_css()

st.markdown("""
<style>
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    .block-container { padding-top: 4rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div>
    <h2 style="font-size: 1.5rem; font-weight: 700; color: #FFFFFF;">Vault</h2>
    <p style="color: #A0AEC0; font-size: 0.9rem;">Your money. No excuses.</p>
</div>
""", unsafe_allow_html=True)

st.info("🚧 Login page — coming Day 2")