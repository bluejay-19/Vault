import streamlit as st
from utils import load_css

st.set_page_config(
    page_title="Vault — Your money. No excuses.",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()

st.markdown("""
<style>
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stApp { background-color: #0F1117 !important; }
    * { box-sizing: border-box; margin: 0; padding: 0; }

    .hero-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 5rem 3rem 4rem;
        gap: 3rem;
    }
    .hero-left { flex: 1; max-width: 520px; }
    .hero-headline {
        font-size: 3.5rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
        margin-bottom: 1rem;
    }
    .hero-tagline {
        font-size: 1.1rem;
        color: #A0AEC0;
        margin-bottom: 2.5rem;
    }
    .cta-primary {
        background-color: #00B37D;
        color: #0F1117;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.75rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .hero-right {
        flex: 1;
        max-width: 560px;
        background: #1A1D2E;
        border-radius: 16px;
        border: 1px solid #2A2D3E;
        padding: 3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 1.5rem;
        min-height: 320px;
    }
    .frank-avatar-landing {
        width: 64px; height: 64px;
        border-radius: 50%;
        background: #1E2130;
        border: 2px solid #00B37D;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.8rem;
        position: relative;
    }
    .frank-online-dot {
        position: absolute;
        top: 2px; right: 2px;
        width: 12px; height: 12px;
        background: #00B37D;
        border-radius: 50%;
        border: 2px solid #1A1D2E;
    }
    .frank-speech-bubble {
        background: #E8920A;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        max-width: 380px;
        position: relative;
    }
    .frank-speech-bubble::before {
        content: '';
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-bottom: 10px solid #E8920A;
    }
    .frank-bubble-text {
        font-size: 1rem;
        color: #1A0F00;
        font-weight: 500;
        line-height: 1.5;
    }
    .features-section {
        padding: 2rem 3rem 5rem;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }
    .feature-card {
        background: #1A1D2E;
        border-radius: 12px;
        border: 1px solid #2A2D3E;
        padding: 2rem 1.75rem;
    }
    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.6rem;
    }
    .feature-desc {
        font-size: 0.9rem;
        color: #A0AEC0;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background-color: #0F1117; min-height: 100vh; font-family: Inter, sans-serif;">
<section class="hero-section">
    <div class="hero-left">
        <h1 class="hero-headline">Your finances.<br>Brutally honest<br>feedback.</h1>
        <p class="hero-tagline">Your money. No excuses.</p>
        <a href="/Login" class="cta-primary">Get Roasted</a>
    </div>
    <div class="hero-right">
        <div class="frank-avatar-landing">🦝<span class="frank-online-dot"></span></div>
        <div class="frank-speech-bubble">
            <p class="frank-bubble-text">$847 on coffee last month?<br>I've seen better financial decisions from raccoons.</p>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

st.markdown("""
<section class="features-section">
    <div class="feature-card">
        <div style="font-size:1.5rem; color:#00B37D; margin-bottom:1rem;">👁️</div>
        <div class="feature-title">Track Everything</div>
        <p class="feature-desc">Upload your statements. See where every dollar goes. No hiding from the truth.</p>
    </div>
    <div class="feature-card">
        <div style="font-size:1.5rem; color:#E8920A; margin-bottom:1rem;">💬</div>
        <div class="feature-title">Frank's Hot Takes</div>
        <p class="feature-desc">AI-powered roasts based on your real spending. He's not mean, just honest.</p>
    </div>
    <div class="feature-card">
        <div style="font-size:1.5rem; color:#00B37D; margin-bottom:1rem;">🛡️</div>
        <div class="feature-title">Private by Default</div>
        <p class="feature-desc">Your data stays yours. Frank judges you, but he doesn't share your secrets.</p>
    </div>
</section>
</div>
""", unsafe_allow_html=True)