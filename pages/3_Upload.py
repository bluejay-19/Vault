import streamlit as st
from utils import load_css, render_sidebar, check_auth

st.set_page_config(
    page_title="Vault — Upload",
    page_icon="🔒",
    layout="wide",
)

load_css()
check_auth()
render_sidebar(active_page="upload")

st.markdown("## Upload Statements")
st.markdown("<p style='color: #A0AEC0;'>CSV or Excel files. Frank will do the rest.</p>", unsafe_allow_html=True)


# Single sheet = single month 
# TODO: Expand it to multi sheet parsing where the isngle excel upload has multiple sheets covering muultiple montths 
