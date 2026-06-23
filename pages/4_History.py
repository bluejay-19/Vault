import streamlit as st
import os
import time
from utils import load_css, render_sidebar, check_auth, get_supabase_client
from groq import Groq

st.set_page_config(
    page_title="Vault — History",
    page_icon="🔒",
    layout="wide",
)

load_css()
check_auth()
render_sidebar(active_page="history")

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    .stButton > button * {
        color: #0F1117 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## History")
st.markdown("<p style='color: #A0AEC0;'>Your spending archive — all the evidence, none of the excuses.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Supabase fetch
supabase = get_supabase_client()
access_token = st.session_state.user.access_token
supabase.auth.set_session(access_token, st.session_state.user.refresh_token)
user_id = st.session_state.user.user.id

response = supabase.table("uploads").select("*").eq("user_id", user_id).order("year", desc=True).order("month", desc=True).execute()
uploads = response.data

if not uploads:
    st.info("No history yet. Upload your first month to get started.")
else:
    currency = uploads[0]["currency"] if uploads[0].get("currency") else "$"

    total_spent_all = sum(u["total_spent"] for u in uploads)
    avg_monthly_savings = sum(u["net_savings"] for u in uploads) / len(uploads)

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown(f"""
                <div style="padding: 0.75rem 0;">
                    <p style="color:#A0AEC0; font-size:13px; margin-bottom:8px;">Total Spent (All Months)</p>
                    <h2 style="color:#FFFFFF; margin:0; font-size:2rem;">{currency}{total_spent_all:,.2f}</h2>
                    <p style="color:#A0AEC0; font-size:12px; margin-top:6px;">Across {len(uploads)} month(s)</p>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            color = "#00B37D" if avg_monthly_savings >= 0 else "#EF4444"
            sign = "+" if avg_monthly_savings >= 0 else ""
            st.markdown(f"""
                <div style="padding: 0.75rem 0;">
                    <p style="color:#A0AEC0; font-size:13px; margin-bottom:8px;">Average Monthly Savings</p>
                    <h2 style="color:{color}; margin:0; font-size:2rem;">{sign}{currency}{avg_monthly_savings:,.2f}</h2>
                    <p style="color:#A0AEC0; font-size:12px; margin-top:6px;">Per month average</p>
                </div>
            """, unsafe_allow_html=True)

    with col3:
        with st.container(border=True):
            st.markdown("<p style='color:#A0AEC0; font-size:13px; margin-bottom:8px;'>Frank's Overall Verdict</p>", unsafe_allow_html=True)

            if "frank_verdict" not in st.session_state:
                try:
                    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                    verdict_prompt = f"""
                    You are Frank, a blunt raccoon financial advisor.
                    Give a 3-4 word brutal but funny verdict on this user's overall finances.
                    Total spent across all months: {currency}{total_spent_all:,.2f}
                    Average monthly savings: {currency}{avg_monthly_savings:,.2f}
                    Number of months tracked: {len(uploads)}
                    Reply with ONLY the short verdict phrase. Examples: "Financially Feral", "Could Be Worse", "Catastrophic Spender", "Surprisingly Decent".
                    """
                    with st.spinner("🦝 Frank is determining your verdict..."):
                        verdict_response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": verdict_prompt}],
                            max_tokens=20
                        )
                    st.session_state.frank_verdict = verdict_response.choices[0].message.content.strip()
                except:
                    st.session_state.frank_verdict = "Financially Questionable"

            st.markdown(f"""
                <div style="background:#E8920A; border-radius:8px; padding:1rem 1.25rem;">
                    <span style="font-size:1.2rem; font-weight:700; color:#1A0F00;">🦝 {st.session_state.frank_verdict}</span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)

            # Cooldown logic
            now = time.time()
            last_regenerated = st.session_state.get("last_verdict_time", 0)
            cooldown_seconds = 30

            if now - last_regenerated < cooldown_seconds:
                remaining = int(cooldown_seconds - (now - last_regenerated))
                st.markdown(f"<p style='color:#A0AEC0; font-size:12px; margin-top:0.5rem;'>Regenerate available in {remaining}s</p>", unsafe_allow_html=True)
            else:
                if st.button("🔄 Regenerate Verdict", use_container_width=True, help="Asks Frank for a fresh verdict"):
                    if "frank_verdict" in st.session_state:
                        del st.session_state.frank_verdict
                    st.session_state.last_verdict_time = time.time()
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]

    def get_verdict_badge(upload):
        spent = upload["total_spent"]
        budget = upload["budget"]
        if budget == 0:
            return "Survivable", "#E8920A", "#1A0F00"
        ratio = spent / budget
        if ratio > 1.1:
            return "Catastrophic", "#EF4444", "#FFFFFF"
        elif ratio > 0.9:
            return "Survivable", "#E8920A", "#1A0F00"
        else:
            return "Not Bad", "#00B37D", "#0F1117"

    def get_biggest_category(upload):
        cb = upload.get("category_breakdown", {})
        if not cb:
            return "N/A"
        filtered = {k: v for k, v in cb.items() if v > 0}
        if not filtered:
            return "N/A"
        return max(filtered, key=filtered.get)

    for i in range(0, len(uploads), 3):
        row_uploads = uploads[i:i+3]
        cols = st.columns(3)

        for col, upload in zip(cols, row_uploads):
            verdict, badge_bg, badge_text = get_verdict_badge(upload)
            biggest_cat = get_biggest_category(upload)
            month_name = month_names[upload["month"]]
            net = upload["net_savings"]
            net_color = "#00B37D" if net >= 0 else "#EF4444"
            net_sign = "+" if net >= 0 else ""

            with col:
                with st.container(border=True):
                    st.markdown(f"""
                        <div style="padding: 0.5rem 0;">
                            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
                                <span style="font-size:1.1rem; font-weight:700; color:#FFFFFF;">{month_name} {upload['year']}</span>
                                <span style="background:{badge_bg}; color:{badge_text}; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600;">{verdict}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                                <span style="color:#A0AEC0; font-size:14px;">Total Spent</span>
                                <span style="color:#EF4444; font-size:14px; font-weight:600;">{currency}{upload['total_spent']:,.2f}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                                <span style="color:#A0AEC0; font-size:14px;">Income</span>
                                <span style="color:#00B37D; font-size:14px; font-weight:600;">{currency}{upload['income']:,.2f}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                                <span style="color:#A0AEC0; font-size:14px;">Budget</span>
                                <span style="color:#FFFFFF; font-size:14px; font-weight:600;">{currency}{upload['budget']:,.2f}</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; margin-bottom:1rem;">
                                <span style="color:#A0AEC0; font-size:14px;">Net Savings</span>
                                <span style="color:{net_color}; font-size:14px; font-weight:600;">{net_sign}{currency}{net:,.2f}</span>
                            </div>
                            <hr style="border-color:#2A2D3E; margin:0.5rem 0;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.75rem;">
                                <span style="color:#A0AEC0; font-size:13px;">Top category</span>
                                <span style="border:1px solid #00B37D; color:#00B37D; padding:3px 12px; border-radius:20px; font-size:13px;">{biggest_cat}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)