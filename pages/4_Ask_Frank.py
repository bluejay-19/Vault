import streamlit as st
from utils import load_css, render_sidebar

st.set_page_config(
    page_title="Vault — Ask Frank",
    page_icon="🔒",
    layout="wide",
)

load_css()
render_sidebar(active_page="askfrank")

st.markdown("## Ask Frank")
st.markdown("<p style='color: #A0AEC0;'>Online · Judging your choices</p>", unsafe_allow_html=True)
st.info("🚧 Ask Frank — coming Day 6")