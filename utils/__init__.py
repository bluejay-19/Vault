import streamlit as st
from pathlib import Path

# shared helper code required by multiple pages 
# each page in the app will import from here 

def load_css():
    """Inject global CSS into the page. Call at the top of every page."""
    css_path = Path(__file__).parent.parent / "styles" / "global.css"
    with open(css_path) as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def check_auth():
    """
    Redirect to login if the user is not authenticated.
    Call at the top of every protected page (everything except Landing and Login).
    """
    if "user" not in st.session_state or st.session_state.user is None:
        st.switch_page("pages/1_Login.py")


def render_sidebar(active_page: str = ""):
    """
    Render the consistent sidebar that appears on all authenticated pages.
    active_page: one of 'dashboard', 'askfrank', 'upload', 'history'
    """
    frank_quips = [
        "Still spending, I see.",
        "I've seen worse... barely.",
        "Your wallet called. It's empty.",
        "Judging your choices.",
        "The numbers don't lie.",
    ]

    # Rotate quip based on a counter in session state
    if "quip_index" not in st.session_state:
        st.session_state.quip_index = 0
    quip = frank_quips[st.session_state.quip_index % len(frank_quips)]

    with st.sidebar:
        # Logo
        st.markdown("""
            <div style="padding: 1.5rem 1rem 1rem; display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 1.5rem;">🔒</span>
                <span style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF;">Vault</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 0 0 1rem; border-color: #2A2D3E;'>", unsafe_allow_html=True)

        # Navigation
        pages = [
            ("dashboard", "🏠", "Dashboard", "pages/2_Dashboard.py"),
            ("askfrank", "💬", "Ask Frank", "pages/4_Ask_Frank.py"),
            ("upload", "📤", "Upload", "pages/3_Upload.py"),
            ("history", "🕐", "History", "pages/5_History.py"),
        ]

        for key, icon, label, path in pages:
            is_active = active_page == key
            bg = "#00C896" if is_active else "transparent"
            color = "#0F1117" if is_active else "#A0AEC0"
            st.markdown(f"""
                <div style="
                    background: {bg};
                    border-radius: 8px;
                    margin-bottom: 4px;
                ">
            """, unsafe_allow_html=True)
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                st.switch_page(path)
            st.markdown("</div>", unsafe_allow_html=True)

        # Frank avatar + quip at the bottom
        st.markdown(f"""
            <div style="
                position: fixed;
                bottom: 1.5rem;
                left: 0;
                width: 220px;
                padding: 0.75rem 1rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
                border-top: 1px solid #2A2D3E;
                background: #1A1D2E;
            ">
                <div style="
                    width: 36px; height: 36px;
                    border-radius: 50%;
                    background: #1E2130;
                    border: 2px solid #00C896;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1.1rem;
                    flex-shrink: 0;
                ">🦝</div>
                <div>
                    <div style="font-size: 13px; font-weight: 600; color: #FFFFFF;">Frank</div>
                    <div style="font-size: 11px; color: #A0AEC0;">{quip}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)