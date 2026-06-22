import os 
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
import time 
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

    fig1 = px.pie(names=labels, values=values, hole=0.5, title="Where Your Money Went")
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    
    # Line Chart - Savings trend 
    chart_data = list(reversed(uploads))
    months = [f"{u['month']}/{u['year']}" for u in chart_data]
    spent_values = [u["total_spent"] for u in chart_data]
    savings_values = [u["net_savings"] for u in chart_data]

    fig2 = go.Figure()
    fig2.update_layout(title="Savings Trend")
    fig2.add_trace(go.Scatter(x=months, y=spent_values, name="Spent", line=dict(color="#E8920A")))
    fig2.add_trace(go.Scatter(x=months, y=savings_values, name="Net Savings", line=dict(color="#00B37D")))

    fig2.update_layout(
        title="Savings Trend",
        xaxis_title="Month",
        yaxis_title=f"Amount ({currency})"
    )
    fig2.update_traces(mode="lines+markers")
    
    # Display charts 
    col_charts, col_frank = st.columns([1.3, 1])
    with col_charts: 
        with st.container(border=True):
            st.plotly_chart(fig1, use_container_width=True)
        with st.container(border=True):
            st.plotly_chart(fig2, use_container_width=True)
    
    # Frank's roast 
    # API call 
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
    You are Frank, a blunt, witty raccoon financial advisor. You roast users based on their REAL spending data, but you always back up the roast with specific numbers and end with genuinely useful advice.

    Their financial data this month:
    - Total spent: {currency}{total_spent:,.2f}
    - Budget: {currency}{budget:,.2f}
    - Income: {currency}{latest['income']:,.2f}
    - Net savings this month: {currency}{latest['net_savings']:,.2f}
    - Category breakdown: {category_breakdown}
    - Biggest category: {biggest_category}

    Write Frank's take in this structure:

    1. Opening roast (1-2 sentences) — punchy, specific, references their biggest category by name and number.
    2. "Where it's going wrong" — name ONE or TWO categories that are eating their budget, with real numbers, in a slightly sarcastic tone.
    3. "What's actually working" — if net savings is positive or a category is notably low, give brief genuine credit. If nothing is working, say so honestly.
    4. "Frank's advice" — exactly ONE specific, actionable recommendation tied directly to their numbers (e.g. "cut your {{category}} spend by {currency}X and you'd hit your savings goal").

    Use line breaks between these four sections. Keep total length to 6-8 sentences. Stay in character — blunt, funny, never generic AI-assistant tone.
    """ 
    start_time = time.time()
    with st.spinner("🦝 Frank is judging your spending..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content":prompt}], 
            max_tokens = 500
        )
    end_time = time.time()
    roast = response.choices[0].message.content
    print(f"[LATENCY] Frank roast generated in {end_time - start_time:.2f} seconds")
    print(f"[FRANK ROAST] user_id: {user_id} | total_spent: {total_spent} | roast_length: {len(roast)}")

    # Display roast 
    with col_frank:
        st.markdown(f"""
        <div style="background:#E8920A; border: 2px solid #00B37D; border-radius: 12px; padding: 1.5rem; height: 100%; overflow-wrap: break-word; word-wrap: break-word;">
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
                <span style="font-size:1.4rem; border: 2px solid #00B37D; border-radius: 50%; padding: 4px; background: #1E2130;">🦝</span>
                <span style="font-size:1.1rem; font-weight:700; color:#1A0F00;">Frank's Take</span>
            </div>
            <div style="color:#1A0F00; line-height:1.6; font-size:1rem;">{roast.replace(chr(10), '<br>')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Ask Frank - question box 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Ask Frank")

        user_question = st.text_input("Got a question about your spending?", placeholder="e.g. Should i cut back on food?")
        ask_submitted = st.button("Ask Frank")

        if ask_submitted and user_question:
            ask_prompt = f"""
            You are Frank, a blunt witty raccoon financial advisor. The user is asking you a direct question about their finances.
            
            Their data this month:
            - Total spent: {currency}{total_spent:,.2f}
            - Budget: {currency}{budget:,.2f}
            - Income: {currency}{latest['income']:,.2f}
            - Net savings: {currency}{latest['net_savings']:,.2f}
            - Category breakdown: {category_breakdown}
            
            Their question: "{user_question}"
        
            Answer in 2-4 sentences, staying in character — blunt, funny, but genuinely helpful and specific to their numbers. 
            If the question is unrelated to personal finance or their spending data, redirect them back to financial topics in Frank's voice without breaking character.
            """
            
            with st.spinner("🦝 Frank is thinking..."):
                ask_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": ask_prompt}],
                    max_tokens=200
                )
            
            frank_answer = ask_response.choices[0].message.content
            print(f"[FRANK Q&A] user_id: {user_id} | question: {user_question} | answer_length: {len(frank_answer)}")

            st.markdown(f"""
            <div style="background:#1E2130; border: 1px solid #00B37D; border-radius: 12px; padding: 1.25rem; margin-top: 1rem;">
                <p style="color:#A0AEC0; font-size:0.85rem; margin-bottom:0.5rem;">You asked: "{user_question}"</p>
                <span style="color:#00B37D; font-weight:700;">🦝 Frank says:</span>
                <p style="color:#FFFFFF; margin-top:0.5rem; line-height:1.6;">{frank_answer}</p>
            </div>
            """, unsafe_allow_html=True)