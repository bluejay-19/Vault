import os 
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
from utils import load_css, render_sidebar, check_auth, get_supabase_client
from groq import Groq

st.set_page_config(
    page_title="Vault — Dashboard",
    page_icon="🔒",
    layout="wide",
)

load_css()
check_auth()
render_sidebar(active_page="dashboard")

st.markdown("## Dashboard")
st.markdown("<p style='color: #A0AEC0;'>Your spending at a glance.</p>", unsafe_allow_html=True)

# Supabase fetch 
# get supabase client and set session 
supabase = get_supabase_client()
access_token = st.session_state.user.access_token
supabase.auth.set_session(access_token, st.session_state.user.refresh_token)

# get user id 
user_id = st.session_state.user.user.id

# fetch query 
response = supabase.table("uploads").select("*").eq("user_id", user_id).order("year", desc=True).order("month", desc=True).execute()

uploads = response.data 

if not uploads: 
    st.info("You have not uploaded anything, go to the uploads tab and upload a sheet for analysing.")

else: 
    latest = uploads[0] # most recent month (already ordered newesst first)

    # parse category_breakdown - it comes back from Supabase as a dict already 
    category_breakdown = latest["category_breakdown"]

    # Summary numbers 
    total_spent = latest["total_spent"]
    biggest_category = max(category_breakdown, key=category_breakdown.get)
    budget = latest["budget"]
    total_savings = sum([upload["net_savings"] for upload in uploads])
    currency = latest["currency"]
 
    if len(uploads) > 1 and uploads[1]["total_spent"] != 0:
        comparison = ((uploads[0]["total_spent"] - uploads[1]["total_spent"]) / uploads[1]["total_spent"]) * 100
    else: 
        comparison = None


    # Summary cards 
    col1, col2, col3, col4 = st.columns(4)

    with col1: 
        with st.container(border=True):
            st.metric("Total Spent", f"{currency}{total_spent:,.2f}")

    with col2: 
        with st.container(border=True):
            st.metric("Biggest Category", biggest_category)

    with col3: 
        with st.container(border=True):
            if comparison is None: 
                st.metric("vs Last Month", "No previous data")
            elif abs(comparison) > 999: 
                sign = "+" if comparison > 0 else "-"
                st.metric("vs Last Month", f"{sign}999%+")
            else: 
                st.metric("vs Last Month", f"{comparison:+.1f}%")

    with col4: 
        with st.container(border=True):
            st.metric("Net Savings to Date", f"{currency}{total_savings:,.2f}")

    # Donut Chart - where your money went 
    filtered = {k: v for k, v in category_breakdown.items() if v > 0}
    labels = filtered.keys()
    values = filtered.values()

    fig = px.pie(names=labels, values=values, hole=0.5, title="Where Your Money Went")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    
    col_donut, col_space = st.columns([2,1])
    with col_donut:
        st.plotly_chart(fig, use_container_width=True)

    # Line Chart - Savings trend 
    chart_data = list(reversed(uploads))
    months = [f"{u['month']}/{u['year']}" for u in chart_data]
    spent_values = [u["total_spent"] for u in chart_data]
    savings_values = [u["net_savings"] for u in chart_data]

    fig2 = go.Figure()
    fig2.update_layout(title="Savings Trend")
    fig2.add_trace(go.Scatter(x=months, y=spent_values, name="Spent", line=dict(color="#E8920A")))
    fig2.add_trace(go.Scatter(x=months, y=savings_values, name="Net Savings", line=dict(color="#00B37D")))
    st.plotly_chart(fig2, use_container_width=True)
    
    # Frank's roast 
    # API call 
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f""" 
    
    You are Frank, a blunt, witty raccoon financial advisor who roasts users based on their REAL spending data. You are funny but not cruel — your jokes always land because they're TRUE, backed by specific numbers.

    Their financial data this month:
    - Total spent: {currency}{total_spent:,.2f}
    - Budget: {currency}{budget:,.2f}
    - Income: {currency}{latest['income']:,.2f}
    - Net savings this month: {currency}{latest['net_savings']:,.2f}
    - Category breakdown: {category_breakdown}
    - Biggest category: {biggest_category}

    Write a roast that:
    1. Opens with a punchy, specific observation about their biggest spending category (use the real number)
    2. Comments on at least one OTHER category that stands out (high or surprisingly low)
    3. States clearly whether they're over, under, or right at budget — with the real numbers
    4. Ends with exactly ONE genuine, specific, actionable piece of financial advice (not generic — tied to their actual data)

    Keep it to 5-7 sentences. Be specific, not generic. Never break character. Never apologize for being blunt.
    """  
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content":prompt}], 
        max_tokens = 400
    )
    roast = response.choices[0].message.content

    # display roast 
    st.markdown(f"""
    <div style="background:#E8920A; border-radius: 12px; padding: 1.5rem;">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.75rem;">
            <span style="font-size:1.5rem;">🦝</span>
            <span style="font-size:1.1rem; font-weight:700; color:#1A0F00;">Frank's Take</span>
        </div>
        <p style="color:#1A0F00; margin:0; line-height:1.6;">{roast}</p>
    </div>
    """, unsafe_allow_html=True)