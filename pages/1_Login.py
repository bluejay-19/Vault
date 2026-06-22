import streamlit as st
from utils import load_css, get_supabase_client

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
    .block-container { 
        padding-top: 3rem !important;
        max-width: 460px !important;
    }
    .stApp { background-color: #0F1117 !important; }
    .stButton > button {
        background-color: #00B37D !important;
        color: #0F1117 !important;
        font-weight: 700 !important;
        opacity: 1 !important;
        border: none !important;
    }
    .stButton > button * {
        color: #0F1117 !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom: 2rem;">
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="3" width="20" height="18" rx="2" stroke="#00B37D" stroke-width="2"/>
        <circle cx="12" cy="12" r="3" stroke="#00B37D" stroke-width="2"/>
        <path d="M12 9V7M12 17v-2M9 12H7M17 12h-2" stroke="#00B37D" stroke-width="2" stroke-linecap="round"/>
        <rect x="17" y="7" width="2" height="3" rx="1" fill="#00B37D"/>
    </svg>
    <h2 style="color:#FFFFFF; margin: 0.5rem 0 0.25rem; font-size:1.5rem;">Vault</h2>
    <p style="color:#A0AEC0; font-size:0.9rem; margin:0;">Your money. No excuses.</p>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):

    mode = st.radio("", ["Login", "Sign Up"], horizontal=True)

    email = st.text_input("Email", placeholder="your@email.com")
    password = st.text_input("Password", placeholder="••••••••", type="password")

    if password and len(password) < 6:
        st.warning("Password must be at least 6 characters.")

    if mode == "Login":
        submitted = st.button("Login", use_container_width=True)
    else:
        submitted = st.button("Sign Up", use_container_width=True)

    if submitted:
        supabase = get_supabase_client()
        try:
            if mode == "Login":
                response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            else:
                response = supabase.auth.sign_up({"email": email, "password": password})
            st.session_state.user = response.session
            st.switch_page("pages/2_Dashboard.py")
        except Exception as e:
            if "Invalid login" in str(e) or "invalid_credentials" in str(e):
                st.error("Wrong email or password.")
            else:
                st.error(f"Something went wrong: {e}")