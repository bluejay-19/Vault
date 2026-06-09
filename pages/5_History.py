import streamlit as st
from utils import load_css, render_sidebar

st.set_page_config(
    page_title="Vault — History",
    page_icon="🔒",
    layout="wide",
)

load_css()
render_sidebar(active_page="history")

st.markdown("## History")
st.markdown("<p style='color: #A0AEC0;'>Your spending archive — all the evidence, none of the excuses.</p>", unsafe_allow_html=True)
st.info("🚧 History — coming Day 7")