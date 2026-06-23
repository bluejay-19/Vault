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
        padding: 1.5rem 3rem 1rem;
        gap: 3rem;
    }
    .hero-left { flex: 1; max-width: 560px; }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(0, 179, 125, 0.1);
        border: 1px solid rgba(0, 179, 125, 0.3);
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        font-size: 0.8rem;
        color: #00B37D;
        margin-bottom: 1.5rem;
    }
    .hero-pill-dot {
        width: 6px; height: 6px;
        background: #00B37D;
        border-radius: 50%;
    }
    .hero-headline {
        font-size: 3rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
        margin-bottom: 1rem;
    }
    .hero-tagline {
        font-size: 1.1rem;
        color: #A0AEC0;
        margin-bottom: 1.5rem;
    }
    .cta-primary {
        background-color: #00B37D;
        color: #0F1117 !important;
        border: none;
        border-radius: 8px;
        padding: 0.85rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .hero-right {
        flex: 1;
        max-width: 480px;
    }
    .frank-speech-top {
        background: #E8920A;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        position: relative;
        max-width: 360px;
        margin-left: auto;
        margin-right: 2rem;
    }
    .frank-speech-top::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-top: 10px solid #E8920A;
    }
    .frank-card {
        background: #1A1D2E;
        border-radius: 16px;
        border: 1px solid #2A2D3E;
        padding: 2rem;
        text-align: center;
    }
    .frank-card-avatar {
        width: 80px; height: 80px;
        border-radius: 50%;
        background: #0F1117;
        border: 2px solid #00B37D;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        margin: 0 auto 1rem;
    }
    .features-section {
        padding: 1.5rem 3rem 2rem;
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
    .feature-icon-circle {
        width: 40px; height: 40px;
        border-radius: 50%;
        background: rgba(0, 179, 125, 0.1);
        border: 1px solid rgba(0, 179, 125, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        margin-bottom: 1.25rem;
    }
    .feature-icon-circle.amber {
        background: rgba(232, 146, 10, 0.1);
        border: 1px solid rgba(232, 146, 10, 0.3);
    }
    .feature-title {
        font-size: 1rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.6rem;
    }
    .feature-desc {
        font-size: 0.88rem;
        color: #A0AEC0;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background-color:#0F1117; font-family:Inter,sans-serif;">
<section class="hero-section">
    <div class="hero-left">
        <div class="hero-pill"><span class="hero-pill-dot"></span>Personal Finance Tracker</div>
        <h1 class="hero-headline">Your finances.<br><span style="color:#00B37D;">Brutally honest</span><br>feedback.</h1>
        <p class="hero-tagline">Your money. No excuses.</p>
        <a href="/Login" class="cta-primary">Get Roasted</a>
    </div>
    <div class="hero-right">
        <div class="frank-speech-top">
            <p style="color:#1A0F00; font-size:0.9rem; font-weight:500; margin:0;">"You spent $340 on miscellaneous last month. We both know what that means."</p>
        </div>
        <div class="frank-card">
            <div class="frank-card-avatar">🦝</div>
            <p style="font-size:0.75rem; color:#A0AEC0; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.25rem;">This Month</p>
            <p style="font-size:2rem; font-weight:800; color:#FFFFFF; margin-bottom:0.25rem;">$4,580 <span style="color:#EF4444;">spent</span></p>
            <p style="font-size:0.85rem; color:#A0AEC0; margin-bottom:1rem;">Budget: $3,500 · Over by $1,080</p>
            <div style="background:#2A2D3E; border-radius:20px; height:8px; width:100%; margin-bottom:0.4rem;">
                <div style="background:#EF4444; height:8px; border-radius:20px; width:100%;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem;">
                <span style="color:#A0AEC0;">$0</span>
                <span style="color:#EF4444;">131% of budget</span>
            </div>
        </div>
    </div>
</section>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<section class="features-section">
    <div class="feature-card">
        <div class="feature-icon-circle">👁️</div>
        <div class="feature-title">Track Everything</div>
        <p class="feature-desc">Upload CSV or Excel statements. Frank catalogues every dollar you pretend you didn't spend.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon-circle amber">💬</div>
        <div class="feature-title">Frank's Hot Takes</div>
        <p class="feature-desc">Unsolicited financial commentary from a raccoon who has seen your transaction history.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon-circle">🛡️</div>
        <div class="feature-title">Private by Default</div>
        <p class="feature-desc">Your spending data stays yours. No ads, no selling your financial shame to third parties.</p>
    </div>
</section>
""", unsafe_allow_html=True)