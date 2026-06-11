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
    .block-container { padding-top: 4rem !important; max-width: 100% !important; }
    .stApp { background-color: #0F1117 !important; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
</style>
""", unsafe_allow_html=True)

mode = st.radio("", ["Login", "Sign Up"], horizontal=True)

email = st.text_input("Email", placeholder="youre@email.com")
password = st.text_input("Password", placeholder="••••••••", type="password")

# Password length warning message 
if password and len(password) < 6: 
    st.warning("Password must be at least 6 characters.")

# TODO: Forgot password reset flow 

# Toggle between Login & Sign Up
if mode == "Login":
    submitted = st.button('Login')
else: 
    submitted = st.button('Sign Up')

# What happens when the button is clicked 
if submitted == True: 
    supabase = get_supabase_client()
    try: 
        if mode == "Login":
            # Login 
            response = supabase.auth.sign_in_with_password({"email": email, "password":password})
        else: 
            # Sign Up 
            response = supabase.auth.sign_up({"email": email, "password": password})
        st.session_state.user = response.session
        st.switch_page("pages/2_Dashboard.py")
    except Exception as e: 
        if "Invalid login" in str(e) or "invalid_credentials" in str(e):
            st.error("Wrong email or password.")
        else: 
            st.error(f"Something went wrong: {e}")
