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
    initial_sidebar_state="expanded"
)

load_css()
check_auth()
render_sidebar(active_page="dashboard")

st.markdown("## Dashboard")

# Supabase fetch 
supabase = get_supabase_client()
access_token = st.session_state.user.access_token
supabase.auth.set_session(access_token, st.session_state.user.refresh_token)
user_id = st.session_state.user.user.id

response = supabase.table("uploads").select("*").eq("user_id", user_id).order("year", desc=True).order("month", desc=True).execute()
uploads = response.data 

if not uploads: 
    st.info("You have not uploaded anything, go to the uploads tab and upload a sheet for analysing.")

else: 
    latest = uploads[0]

    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    month_label = f"{month_names[latest['month']]} {latest['year']}"
    st.markdown(f"<p style='color: #A0AEC0;'>Your spending at a glance &nbsp;·&nbsp; <span style='color:#00B37D;'>{month_label}</span></p>", unsafe_allow_html=True)

    category_breakdown = latest["category_breakdown"]
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
            st.metric("Income", f"{currency}{latest['income']:,.2f}")

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
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Budget vs Actual progress bar
    budget_pct = min((total_spent / budget * 100), 100) if budget > 0 else 0
    over_budget = total_spent > budget
    bar_color = "#EF4444" if over_budget else "#00B37D"
    over_under = f"{currency}{abs(total_spent - budget):,.2f} {'over' if over_budget else 'under'} budget"

    st.markdown(f"""
    <div style="background:#1E2130; border: 1px solid #2A2D3E; border-radius: 12px; padding: 1.25rem 1.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
            <span style="color:#FFFFFF; font-weight:600;">🎯 Budget vs Actual</span>
            <span style="color:{bar_color}; font-weight:600; font-size:0.9rem;">{currency}{total_spent:,.2f} / {currency}{budget:,.2f} — {over_under}</span>
        </div>
        <div style="background:#2A2D3E; border-radius:20px; height:12px; width:100%;">
            <div style="background:{bar_color}; width:{budget_pct}%; height:12px; border-radius:20px; transition: width 0.3s ease;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:0.4rem;">
            <span style="color:#A0AEC0; font-size:12px;">{currency}0</span>
            <span style="color:#A0AEC0; font-size:12px;">{currency}{budget:,.2f} budget</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    filtered = {k: v for k, v in category_breakdown.items() if v > 0}
    labels = list(filtered.keys())
    values = list(filtered.values())

    # Donut chart — hover shows category + amount + percentage
    fig1 = px.pie(
        names=labels,
        values=values,
        hole=0.5,
        title="Where Your Money Went"
    )
    fig1.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>' + currency + '%{value:,.2f}<br>%{percent}<extra></extra>'
    )
    fig1.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF", size=13),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(color="#A0AEC0", size=13),
        ),
        margin=dict(t=40, b=20, l=20, r=120)
    )

    # Line chart
    chart_data = list(reversed(uploads))
    months = [f"{u['month']}/{u['year']}" for u in chart_data]
    spent_values = [u["total_spent"] for u in chart_data]
    savings_values = [u["net_savings"] for u in chart_data]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=months, y=spent_values, name="Spent",
        line=dict(color="#E8920A", width=2),
        mode="lines+markers"
    ))
    fig2.add_trace(go.Scatter(
        x=months, y=savings_values, name="Net Savings",
        line=dict(color="#00B37D", width=2),
        mode="lines+markers"
    ))
    fig2.update_layout(
        height=420,
        title="Savings Trend",
        xaxis_title="Month",
        yaxis_title=f"Amount ({currency})",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        legend=dict(font=dict(color="#FFFFFF")),
        xaxis=dict(gridcolor="#2A2D3E"),
        yaxis=dict(gridcolor="#2A2D3E"),
        margin=dict(t=40, b=20, l=20, r=20)
    )

    col_donut, col_line = st.columns(2)

    with col_donut:
        with st.container(border=True):
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding: 0.25rem 0.5rem 0.75rem;">
                <span style="color:#A0AEC0; font-size:14px;">Biggest category</span>
                <span style="background:#00B37D; color:#0F1117; padding:4px 14px; border-radius:20px; font-size:13px; font-weight:600;">{biggest_category.title()}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_line:
        with st.container(border=True):
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Frank's roast
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def call_groq_with_retry(client, messages, max_tokens, retries=2):
        for attempt in range(retries):
            try: 
                return client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    max_tokens=max_tokens
                )
            except Exception as e: 
                if attempt < retries - 1:
                    time.sleep(1)
                else: 
                    raise e 
            
    prompt = f"""
    You are Frank, a blunt, witty raccoon financial advisor. You roast users based on their REAL spending data, but you always back up the roast with specific numbers and end with genuinely useful advice.

    Their financial data this month:
    - Total spent: {currency}{total_spent:,.2f}
    - Budget: {currency}{budget:,.2f}
    - Income: {currency}{latest['income']:,.2f}
    - Net savings this month: {currency}{latest['net_savings']:,.2f}
    - Category breakdown: {category_breakdown}
    - Biggest category: {biggest_category}

    Write Frank's take in this structure — use these exact labels on their own line before each section:

    OBSERVATION
    (1-2 sentences — punchy, specific, references biggest category by name and amount)

    GOING WRONG
    (1-2 sentences — name one or two categories eating the budget with real numbers, sarcastic tone)

    WORKING
    (1 sentence — genuine credit if savings positive or a category is low. If nothing working, say so honestly)

    ACTION
    (1 sentence — exactly one specific actionable recommendation tied to their real numbers)

    Keep total length to 6-8 sentences. Stay in character — blunt, funny, never generic AI-assistant tone.
    """ 

    with st.spinner("🦝 Frank is judging your spending..."):
        start_time = time.time()
        response = call_groq_with_retry(
            client,
            messages=[
                {"role": "system", "content": "You are Frank, a blunt witty raccoon financial advisor. You roast users based on their REAL spending data with specific numbers. Never break character. Never give generic advice. Always end with exactly one specific actionable recommendation tied to the user's actual numbers."},
                {"role": "user", "content": prompt}], 
            max_tokens=500
        )
        end_time = time.time()

    roast = response.choices[0].message.content
    print(f"[LATENCY] Frank roast generated in {end_time - start_time:.2f} seconds")
    print(f"[FRANK ROAST] user_id: {user_id} | total_spent: {total_spent} | roast_length: {len(roast)}")

    formatted_roast = roast
    for label in ["OBSERVATION", "GOING WRONG", "WORKING", "ACTION"]:
        formatted_roast = formatted_roast.replace(
            label,
            f'<span style="color:#E8920A; font-size:0.75rem; font-weight:700; letter-spacing:0.05em;">{label}</span>'
        )

    st.markdown(f"""
    <div style="background:transparent; border: 1px solid #E8920A; border-radius: 12px; padding: 1.5rem; overflow-wrap: break-word;">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
            <span style="font-size:1.4rem; border: 2px solid #00B37D; border-radius: 50%; padding: 4px; background: #1E2130;">🦝</span>
            <span style="font-size:1.1rem; font-weight:700; color:#E8920A;">Frank's Take</span>
        </div>
        <div style="color:#FFFFFF; line-height:1.8; font-size:0.95rem;">{formatted_roast.replace(chr(10), '<br>')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Ask Frank
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#1E2130; border: 1px solid #2A2D3E; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1rem;">
        <span style="font-size:1rem; font-weight:700; color:#FFFFFF;">Ask Frank</span>
        <p style="color:#A0AEC0; font-size:0.85rem; margin:0.25rem 0 0;">Got a question about your spending? Frank won't sugarcoat it.</p>
    </div>
    """, unsafe_allow_html=True)

    user_question = st.text_input("", placeholder="e.g. Should I cut back on food?", label_visibility="collapsed")
    ask_submitted = st.button("Ask Frank", use_container_width=False)

    if ask_submitted and user_question:
        import re 
        user_question_clean = re.sub(r'<[^>]+>', '', user_question).strip()            
        ask_prompt = f"""
        The user is asking you a direct question about their finances.
            
        Their data this month:
        - Total spent: {currency}{total_spent:,.2f}
        - Budget: {currency}{budget:,.2f}
        - Income: {currency}{latest['income']:,.2f}
        - Net savings: {currency}{latest['net_savings']:,.2f}
        - Category breakdown: {category_breakdown}
            
        Their question: "{user_question_clean}"
        
        Answer in 2-4 sentences, staying in character — blunt, funny, but genuinely helpful and specific to their numbers. 
        If the question is unrelated to personal finance or their spending data, redirect them back to financial topics in Frank's voice without breaking character.
        """    
        with st.spinner("🦝 Frank is thinking..."):
            ask_response = call_groq_with_retry(
                client,
                messages=[
                    {"role": "system", "content": "You are Frank, a blunt witty raccoon financial advisor. Answer questions about the user's finances using their real spending data. Stay in character — blunt, funny, specific. If the question is unrelated to personal finance, redirect back to financial topics in Frank's voice."},
                    {"role": "user", "content": ask_prompt}
                ],
                max_tokens=200
            )
            
        frank_answer = ask_response.choices[0].message.content
        print(f"[FRANK Q&A] user_id: {user_id} | question: {user_question_clean} | answer_length: {len(frank_answer)}")

        st.markdown(f"""
        <div style="background:#1E2130; border: 1px solid #00B37D; border-radius: 12px; padding: 1.25rem; margin-top: 1rem;">
            <p style="color:#A0AEC0; font-size:0.85rem; margin-bottom:0.5rem;">You asked: "{user_question_clean}"</p>
            <span style="color:#00B37D; font-weight:700;">🦝 Frank says:</span>
            <p style="color:#FFFFFF; margin-top:0.5rem; line-height:1.6;">{frank_answer}</p>
        </div>
        """, unsafe_allow_html=True)