import streamlit as st
from utils import load_css, render_sidebar

st.set_page_config(
    page_title="Vault — Upload",
    page_icon="🔒",
    layout="wide",
)

load_css()
render_sidebar(active_page="upload")

st.markdown("## Upload Statements")
st.markdown("<p style='color: #A0AEC0;'>CSV or Excel files. Frank will do the rest.</p>", unsafe_allow_html=True)
st.info("🚧 Upload — coming Day 3")