import streamlit as st
import requests
import time
import os

API_URL      = "http://localhost:8000"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_KEY = os.getenv("GROQ_API_KEY", "your-groq-key-here")

st.set_page_config(
    page_title="MediPredict — Diabetes Risk AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'DM Mono', monospace;
    background: #0a0e14 !important;
    color: #c9d1d9 !important;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 1rem 2rem !important; max-width: 100% !important; }

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1e2d3d;
}
.brand-hex {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #00d2be, #00a896);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    flex-shrink: 0;
}
.brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #e6edf3;
    letter-spacing: -0.5px;
}
.brand-tag {
    font-size: 0.65rem;
    color: #00d2be;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.section-label {
    font-size: 0.6rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #00d2be;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e2d3d;
}

div[data-testid="stNumberInput"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #8b949e !important;
}
div[data-testid="stNumberInput"] input {
    background: #161b22 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 6px !important;
    color: #e6edf3 !important;
    font-family: 'DM Mono', monospace !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #00d2be !important;
    box-shadow: 0 0 0 2px rgba(0,210,190,0.1) !important;
}

div[data-testid="stButton"] button {
    width: 100% !important;
    background: linear-gradient(135deg, #00d2be, #00a896) !important;
    color: #0a0e14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.85rem !important;
    margin-top: 1rem !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0,210,190,0.25) !important;
}

.result-card { border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; position: relative; overflow: hidden; }
.result-high { background: linear-gradient(135deg, #1a0a0a, #1f1010); border: 1px solid #ff4d4d33; }
.result-low  { background: linear-gradient(135deg, #0a1a14, #0d1f18); border: 1px solid #00d2be33; }
.result-high::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg,#ff4d4d,#ff8c42); }
.result-low::before  { content:''; position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg,#00d2be,#00ff88); }
.result-label-high { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; color:#ff6b6b; margin-bottom:0.5rem; }
.result-label-low  { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; color:#00d2be; margin-bottom:0.5rem; }
.result-advice { font-size:0.82rem; line-height:1.7; color:#8b949e; }

.metric-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.75rem; margin-bottom:1rem; }
.metric-tile { background:#161b22; border:1px solid #1e2d3d; border-radius:10px; padding:1rem; text-align:center; }
.metric-value { font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800; color:#e6edf3; }
.metric-name  { font-size:0.6rem; letter-spacing:2px; text-transform:uppercase; color:#8b949e; margin-top:3px; }

.prob-bar-wrap { background:#161b22; border:1px solid #1e2d3d; border-radius:10px; padding:1.2rem; margin-bottom:1rem; }
.prob-bar-label { font-size:0.6rem; letter-spacing:3px; text-transform:uppercase; color:#8b949e; margin-bottom:0.75rem; }
.prob-bar-track { background:#0d1117; border-radius:99px; height:8px; overflow:hidden; margin-bottom:0.4rem; }
.prob-bar-fill-high { height:100%; border-radius:99px; background:linear-gradient(90deg,#ff4d4d,#ff8c42); }
.prob-bar-fill-low  { height:100%; border-radius:99px; background:linear-gradient(90deg,#00d2be,#00ff88); }
.prob-bar-pct { font-family:'Syne',sans-serif; font-size:0.85rem; font-weight:700; text-align:right; }

.chat-container {
    background: #0d1117;
    border: 1px solid #1e2d3d;
    border-radius: 12px;
    padding: 1.25rem;
    height: 340px;
    overflow-y: auto;
    margin-bottom: 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    scroll-behavior: smooth;
}
.chat-msg-bot  { display:flex; gap:10px; align-items:flex-start; }
.chat-msg-user { display:flex; gap:10px; align-items:flex-start; flex-direction:row-reverse; }
.chat-avatar-bot {
    width:28px; height:28px;
    background: linear-gradient(135deg,#00d2be,#00a896);
    clip-path: polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
    flex-shrink:0; margin-top:2px;
}
.chat-avatar-user {
    width:28px; height:28px;
    background:#1e2d3d; border-radius:50%;
    flex-shrink:0; margin-top:2px;
    display:flex; align-items:center; justify-content:center;
    font-size:0.75rem; color:#8b949e;
}
.chat-bubble-bot {
    background:#161b22; border:1px solid #1e2d3d;
    border-radius:0 10px 10px 10px;
    padding:0.75rem 1rem; font-size:0.8rem;
    line-height:1.6; color:#c9d1d9; max-width:85%;
}
.chat-bubble-user {
    background:rgba(0,210,190,0.1); border:1px solid rgba(0,210,190,0.2);
    border-radius:10px 0 10px 10px;
    padding:0.75rem 1rem; font-size:0.8rem;
    line-height:1.6; color:#c9d1d9; max-width:85%;
}

div[data-testid="stTextInput"] input {
    background:#161b22 !important; border:1px solid #1e2d3d !important;
    border-radius:8px !important; color:#e6edf3 !important;
    font-family:'DM Mono',monospace !important; font-size:0.85rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color:#00d2be !important;
    box-shadow:0 0 0 2px rgba(0,210,190,0.1) !important;
}
div[data-testid="stTextInput"] label {
    font-size:0.6rem !important; letter-spacing:3px !important;
    text-transform:uppercase !important; color:#8b949e !important;
}

.chip-row { display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:0.75rem; }
.chip {
    background:#161b22; border:1px solid #1e2d3d;
    border-radius:99px; padding:0.3rem 0.75rem;
    font-size:0.7rem; color:#8b949e; cursor:pointer; transition:all 0.2s;
}
.chip:hover { border-color:#00d2be; color:#00d2be; }

.model-strip {
    background:#161b22; border:1px solid #1e2d3d;
    border-radius:8px; padding:0.85rem 1.5rem;
    display:flex; justify-content:space-between; align-items:center; margin-top:1rem;
}
.model-strip-val { font-family:'Syne',sans-serif; font-size:0.85rem; font-weight:700; color:#00d2be; }
.model-strip-key { font-size:0.55rem; letter-spacing:2px; text-transform:uppercase; color:#8b949e; margin-top:2px; }

.disclaimer {
    margin-top:0.75rem; padding:0.6rem 0.9rem;
    background:rgba(255,180,0,0.05); border:1px solid rgba(255,180,0,0.15);
    border-radius:6px; font-size:0.65rem; color:#8b6914;
}

div[data-testid="column"] { padding: 0 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "bot", "text": "👋 Hi! I'm your MediPredict assistant. I can help you understand your diabetes risk results, explain what each health metric means, or answer general questions. What would you like to know?"}
    ]
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ── BRAND HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand">
    <div class="brand-hex"></div>
    <div>
        <div class="brand-name">MediPredict</div>
        <div class="brand-tag">Diabetes Risk AI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── THREE COLUMN LAYOUT ───────────────────────────────────────────────────────
col_form, col_result, col_chat = st.columns([1, 1, 1], gap="large")

# ════════════════════════════════════════════════════════════════════════════
# COLUMN 1 — INPUT FORM
# ════════════════════════════════════════════════════════════════════════════
with col_form:
    st.markdown('<div class="section-label">Patient Metrics</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        pregnancies    = st.number_input("Pregnancies",         min_value=0,   max_value=20,    value=2,     step=1)
        glucose        = st.number_input("Glucose mg/dL",       min_value=1.0, max_value=300.0, value=110.0, step=1.0)
        blood_pressure = st.number_input("Blood Pressure mmHg", min_value=1.0, max_value=200.0, value=72.0,  step=1.0)
        skin_thickness = st.number_input("Skin Thickness mm",   min_value=1.0, max_value=100.0, value=20.0,  step=0.5)
    with c2:
        insulin           = st.number_input("Insulin mu U/ml",  min_value=1.0, max_value=900.0, value=80.0,  step=1.0)
        bmi               = st.number_input("BMI",              min_value=1.0, max_value=70.0,  value=25.0,  step=0.1)
        diabetes_pedigree = st.number_input("Pedigree Score",   min_value=0.0, max_value=3.0,   value=0.47,  step=0.01)
        age               = st.number_input("Age (years)",      min_value=1,   max_value=120,   value=30,    step=1)

    bmi_cat   = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
    bmi_color = "#00d2be" if bmi_cat == "Normal" else "#ff8c42" if bmi_cat in ["Overweight","Underweight"] else "#ff6b6b"
    st.markdown(f'<div style="font-size:0.68rem; color:{bmi_color}; letter-spacing:1px; margin:0.4rem 0 0.8rem;">BMI — {bmi_cat.upper()}</div>', unsafe_allow_html=True)

    run = st.button("⬡  Run Risk Assessment")

    st.markdown("""
    <div class="disclaimer">
        ⚠ FOR EDUCATIONAL USE ONLY — Not a substitute for professional medical diagnosis.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="model-strip" style="margin-top:0.75rem;">
        <div style="text-align:center"><div class="model-strip-val">75.3%</div><div class="model-strip-key">Accuracy</div></div>
        <div style="text-align:center"><div class="model-strip-val">0.826</div><div class="model-strip-key">ROC-AUC</div></div>
        <div style="text-align:center"><div class="model-strip-val">768</div><div class="model-strip-key">Samples</div></div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# COLUMN 2 — RESULTS
# ════════════════════════════════════════════════════════════════════════════
with col_result:
    st.markdown('<div class="section-label">Risk Analysis</div>', unsafe_allow_html=True)

    if run:
        payload = {
            "pregnancies": int(pregnancies), "glucose": float(glucose),
            "blood_pressure": float(blood_pressure), "skin_thickness": float(skin_thickness),
            "insulin": float(insulin), "bmi": float(bmi),
            "diabetes_pedigree": float(diabetes_pedigree), "age": int(age)
        }
        with st.spinner("Analysing..."):
            time.sleep(0.3)
            try:
                response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
                result   = response.json()
                st.session_state.last_result = result
                st.session_state.last_result["age"]     = int(age)
                st.session_state.last_result["bmi"]     = float(bmi)
                st.session_state.last_result["glucose"] = float(glucose)

                risk    = result["risk_label"]
                prob    = result["risk_probability"]
                bot_msg = f"I've analysed the results — **{risk}** with a {prob*100:.1f}% probability score. Would you like me to explain what this means or what steps to take next?"
                st.session_state.chat_history.append({"role": "bot", "text": bot_msg})

            except requests.exceptions.ConnectionError:
                st.error("⬡ API offline. Run: uvicorn app.main:app --reload")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.last_result:
        r         = st.session_state.last_result
        risk      = r["risk_label"]
        prob      = r["risk_probability"]
        advice    = r["advice"]
        is_high   = risk == "High Risk"
        card_cls  = "result-high" if is_high else "result-low"
        label_cls = "result-label-high" if is_high else "result-label-low"
        icon      = "⚠" if is_high else "✓"
        fill_cls  = "prob-bar-fill-high" if is_high else "prob-bar-fill-low"
        pct_color = "#ff6b6b" if is_high else "#00d2be"
        conf      = "VERY HIGH" if prob >= 0.75 else "HIGH" if prob >= 0.55 else "MODERATE" if prob >= 0.40 else "LOW"

        st.markdown(f"""
        <div class="result-card {card_cls}">
            <div class="{label_cls}">{icon} {risk}</div>
            <div class="result-advice">{advice}</div>
        </div>
        <div class="metric-grid">
            <div class="metric-tile">
                <div class="metric-value" style="color:{pct_color}">{prob*100:.1f}%</div>
                <div class="metric-name">Probability</div>
            </div>
            <div class="metric-tile">
                <div class="metric-value">{conf}</div>
                <div class="metric-name">Confidence</div>
            </div>
            <div class="metric-tile">
                <div class="metric-value">{r.get('age','—')}</div>
                <div class="metric-name">Patient Age</div>
            </div>
        </div>
        <div class="prob-bar-wrap">
            <div class="prob-bar-label">Risk Probability Score</div>
            <div class="prob-bar-track">
                <div class="{fill_cls}" style="width:{prob*100:.1f}%"></div>
            </div>
            <div class="prob-bar-pct" style="color:{pct_color}">{prob*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:4rem 1rem; color:#8b949e;">
            <div style="font-size:2.5rem; margin-bottom:1rem;">⬡</div>
            <div style="font-family:'Syne',sans-serif; font-size:1rem; color:#e6edf3; margin-bottom:0.5rem;">Awaiting Assessment</div>
            <div style="font-size:0.8rem; line-height:1.6;">Enter patient metrics and run the assessment to see results here.</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# COLUMN 3 — AI CHATBOT
# ════════════════════════════════════════════════════════════════════════════
with col_chat:
    st.markdown('<div class="section-label">AI Assistant</div>', unsafe_allow_html=True)

    chat_html = '<div class="chat-container">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "bot":
            chat_html += f'''
            <div class="chat-msg-bot">
                <div class="chat-avatar-bot"></div>
                <div class="chat-bubble-bot">{msg["text"]}</div>
            </div>'''
        else:
            chat_html += f'''
            <div class="chat-msg-user">
                <div class="chat-avatar-user">👤</div>
                <div class="chat-bubble-user">{msg["text"]}</div>
            </div>'''
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    st.markdown("""
    <div class="chip-row">
        <span class="chip">What is glucose?</span>
        <span class="chip">What does High Risk mean?</span>
        <span class="chip">How to reduce risk?</span>
        <span class="chip">What is BMI?</span>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_input("Ask anything...", key="chat_input", label_visibility="collapsed", placeholder="e.g. What does my result mean?")
    send = st.button("Send Message", key="send_btn")

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        result_context = ""
        if st.session_state.last_result:
            r = st.session_state.last_result
            result_context = f"""
The patient's latest assessment:
- Risk: {r['risk_label']}
- Probability: {r['risk_probability']*100:.1f}%
- Glucose: {r.get('glucose','N/A')} mg/dL
- BMI: {r.get('bmi','N/A')}
- Age: {r.get('age','N/A')}
- Advice: {r['advice']}
"""

        system_prompt = f"""You are a friendly, empathetic medical AI assistant inside MediPredict, a diabetes risk prediction app.
Help patients understand their results, explain medical terms simply, and provide general health guidance.
{result_context}
Rules:
- Keep responses concise (2-4 sentences)
- Use simple non-technical language
- Always remind users to consult a real doctor
- Be warm, encouraging and supportive
- Never diagnose or prescribe"""

        try:
            # Build messages — filter so roles strictly alternate user/assistant
            api_messages = []
            for m in st.session_state.chat_history:
                role = "user" if m["role"] == "user" else "assistant"
                if api_messages and api_messages[-1]["role"] == role:
                    api_messages[-1]["content"] += "\n" + m["text"]
                else:
                    api_messages.append({"role": role, "content": m["text"]})

            response = requests.post(
                GROQ_API_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {GROQ_KEY}"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "max_tokens": 500,
                    "messages": [{"role": "system", "content": system_prompt}] + api_messages
                },
                timeout=20
            )
            data      = response.json()
            bot_reply = data["choices"][0]["message"]["content"]

        except Exception as e:
            bot_reply = f"Sorry, I couldn't connect to the AI right now. (Error: {str(e)[:80]})"

        st.session_state.chat_history.append({"role": "bot", "text": bot_reply})
        st.rerun()