import streamlit as st
from risk_analyzer import analyze_message

st.set_page_config(
    page_title="ScamShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: #f7f9fc;
    color: #182230;
}

.block-container {
    max-width: 1120px;
    padding-top: 2.8rem;
    padding-bottom: 3rem;
}

/* Header */
.header {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 0 0 18px;
    border-bottom: 1px solid #e7ebf2;
}

.brand {
    display:flex;
    align-items:center;
    gap:10px;
}

.brand-icon {
    width:40px;
    height:40px;
    border-radius:11px;
    background:#172033;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
}

.brand-name {
    font-size:20px;
    font-weight:800;
    letter-spacing:-.4px;
}

.brand-name span { color:#3478e5; }

.engine {
    display:flex;
    align-items:center;
    gap:7px;
    color:#18794e;
    background:#effaf4;
    border:1px solid #d5efdf;
    padding:7px 11px;
    border-radius:20px;
    font-size:11px;
    font-weight:700;
}

/* Hero */
.hero {
    text-align:center;
    padding:42px 10px 28px;
}

.badge {
    display:inline-block;
    color:#2867c7;
    background:#edf4ff;
    border:1px solid #d9e8ff;
    border-radius:20px;
    padding:6px 11px;
    font-size:10px;
    font-weight:800;
    letter-spacing:.8px;
}

.hero h1 {
    font-size:38px;
    line-height:1.15;
    letter-spacing:-1.2px;
    margin:15px 0 10px;
    color:#111827;
}

.hero h1 span { color:#3478e5; }

.hero p {
    max-width:650px;
    margin:auto;
    color:#6b7688;
    font-size:14px;
    line-height:1.65;
}

/* Input */
.input-card {
    background:#fff;
    border:1px solid #e1e6ee;
    border-radius:16px;
    padding:20px 22px 18px;
    box-shadow:0 8px 25px rgba(20,32,50,.045);
}

.input-title {
    font-size:15px;
    font-weight:750;
    margin-bottom:4px;
}

.input-help {
    color:#7c8798;
    font-size:11px;
    margin-bottom:13px;
}

textarea {
    background:#fbfcfe !important;
    border:1px solid #dce2eb !important;
    border-radius:10px !important;
    color:#182230 !important;
    font-size:13px !important;
}

textarea:focus {
    border-color:#3478e5 !important;
    box-shadow:0 0 0 2px rgba(52,120,229,.09) !important;
}

.stButton > button {
    background:#172033;
    color:#fff;
    border:0;
    border-radius:9px;
    min-height:42px;
    font-size:12px;
    font-weight:700;
    letter-spacing:.2px;
}

.stButton > button:hover {
    background:#27344c;
    color:#fff;
}

/* Section */
.section {
    margin:27px 0 12px;
    font-size:16px;
    font-weight:800;
    color:#182230;
}

/* Metrics */
.metric {
    background:#fff;
    border:1px solid #e1e6ee;
    border-radius:13px;
    padding:15px 17px;
    box-shadow:0 5px 18px rgba(20,32,50,.03);
}

.metric-label {
    font-size:10px;
    color:#7b8798;
    font-weight:700;
    letter-spacing:.55px;
}

.metric-value {
    font-size:25px;
    font-weight:800;
    margin-top:5px;
}

/* Threat banner */
.threat {
    margin-top:12px;
    background:#172033;
    border-radius:14px;
    padding:19px 21px;
    color:white;
}

.threat-top {
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.threat-label {
    color:#aeb8c9;
    font-size:9px;
    font-weight:700;
    letter-spacing:1px;
}

.threat-score {
    font-size:34px;
    font-weight:800;
    margin-top:4px;
}

.threat-level {
    font-size:12px;
    font-weight:700;
    color:#ffb4b2;
}

.track {
    height:7px;
    background:#364156;
    border-radius:20px;
    overflow:hidden;
    margin-top:14px;
}

.fill {
    height:100%;
    background:#ef5350;
    border-radius:20px;
}

/* Result cards */
.card {
    background:#fff;
    border:1px solid #e1e6ee;
    border-radius:14px;
    padding:18px;
    min-height:150px;
    box-shadow:0 5px 18px rgba(20,32,50,.03);
}

.card-title {
    font-size:13px;
    font-weight:800;
    margin-bottom:13px;
}

.indicator {
    background:#fff7f7;
    border:1px solid #f7dddd;
    border-left:3px solid #ef5350;
    border-radius:7px;
    padding:8px 10px;
    margin:6px 0;
    color:#475467;
    font-size:11px;
}

.no-risk {
    background:#effaf4;
    border:1px solid #d5efdf;
    border-radius:8px;
    padding:10px;
    color:#18794e;
    font-size:11px;
}

.model {
    margin:10px 0 15px;
}

.model-head {
    display:flex;
    justify-content:space-between;
    font-size:11px;
    color:#475467;
    margin-bottom:6px;
}

.model-track {
    height:7px;
    background:#edf0f5;
    border-radius:20px;
    overflow:hidden;
}

.model-fill {
    height:100%;
    background:#3478e5;
    border-radius:20px;
}

/* Recommendation */
.recommendation {
    background:#fff;
    border:1px solid #e1e6ee;
    border-left:4px solid #3478e5;
    border-radius:12px;
    padding:16px 18px;
    color:#536071;
    font-size:12px;
    line-height:1.7;
}

/* Features */
.feature {
    background:#fff;
    border:1px solid #e1e6ee;
    border-radius:12px;
    padding:16px;
    min-height:125px;
}

.feature-icon { font-size:18px; }

.feature-title {
    font-size:12px;
    font-weight:800;
    margin-top:7px;
}

.feature-text {
    color:#7b8798;
    font-size:10.5px;
    line-height:1.55;
    margin-top:5px;
}

.footer {
    text-align:center;
    color:#98a2b3;
    font-size:10px;
    margin-top:35px;
    padding-top:20px;
    border-top:1px solid #e7ebf2;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div class="brand-name">Scam<span>Shield</span> AI</div>
    </div>
    <div class="engine">● AI ENGINE ONLINE</div>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="badge">AI-POWERED THREAT DETECTION</div>
    <h1>Know the risk before you<br><span>click, reply, or pay.</span></h1>
    <p>Analyze suspicious messages with machine learning, neural networks, and security-focused risk indicators.</p>
</div>
""", unsafe_allow_html=True)

# Input
st.markdown("""
<div class="input-card">
    <div class="input-title">🔍 Analyze a suspicious message</div>
    <div class="input-help">Paste an SMS, email, WhatsApp message, or suspicious text below.</div>
</div>
""", unsafe_allow_html=True)

message = st.text_area(
    "Message",
    height=145,
    label_visibility="collapsed",
    placeholder="Example: URGENT! Your account has been compromised. Click https://example.com and verify your OTP..."
)

if st.button("🔎  ANALYZE MESSAGE", use_container_width=True):
    if not message.strip():
        st.warning("Please paste a message before analyzing it.")
    else:
        with st.spinner("Analyzing threat signals..."):
            result = analyze_message(message)

        score = min(max(float(result["risk_score"]), 0), 100)
        ml = min(max(float(result["ml_score"]), 0), 100)
        nn = min(max(float(result["nn_score"]), 0), 100)

        st.markdown('<div class="section">Threat Assessment</div>', unsafe_allow_html=True)

        a, b, c = st.columns(3)
        for col, label, value in [
            (a, "FINAL RISK SCORE", score),
            (b, "LOGISTIC REGRESSION", ml),
            (c, "NEURAL NETWORK", nn),
        ]:
            with col:
                st.markdown(
                    f'<div class="metric"><div class="metric-label">{label}</div>'
                    f'<div class="metric-value">{value:.1f}%</div></div>',
                    unsafe_allow_html=True
                )

        level = str(result["risk_level"])
        level_color = "#ffb4b2" if score >= 75 else "#ffd58a" if score >= 50 else "#8ee0b7"

        st.markdown(
            f'<div class="threat">'
            f'<div class="threat-top"><div><div class="threat-label">OVERALL THREAT LEVEL</div>'
            f'<div class="threat-score">{score:.0f}%</div></div>'
            f'<div class="threat-level" style="color:{level_color}">● {level}</div></div>'
            f'<div class="track"><div class="fill" style="width:{score:.0f}%"></div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        left, right = st.columns(2)

        with left:
            st.markdown('<div class="section">🚨 Detected Risk Indicators</div>', unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            indicators = result.get("indicators", [])
            if indicators:
                for item in indicators:
                    st.markdown(f'<div class="indicator">⚠ {item}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="no-risk">✓ No major scam indicators detected.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="section">🧠 Model Confidence</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="card"><div class="card-title">AI prediction comparison</div>'
                f'<div class="model"><div class="model-head"><span>Logistic Regression</span><span>{ml:.1f}%</span></div>'
                f'<div class="model-track"><div class="model-fill" style="width:{ml:.1f}%"></div></div></div>'
                f'<div class="model"><div class="model-head"><span>Neural Network</span><span>{nn:.1f}%</span></div>'
                f'<div class="model-track"><div class="model-fill" style="width:{nn:.1f}%"></div></div></div>'
                f'<div style="color:#7b8798;font-size:10.5px;line-height:1.5;">'
                f'The final score combines model predictions with rule-based security signals.</div></div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="section">🛡 Recommended Action</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="recommendation"><b>{level}</b><br>{result["recommendation"]}</div>',
            unsafe_allow_html=True
        )

# Features
st.markdown('<div class="section">How ScamShield works</div>', unsafe_allow_html=True)
x, y, z = st.columns(3)

features = [
    (x, "🧠", "Dual AI Detection", "Two ML approaches estimate whether the message contains scam-like patterns."),
    (y, "🔎", "Threat Indicators", "Checks urgency, links, financial requests, prizes, OTPs, passwords, and phone numbers."),
    (z, "🛡️", "Safety Guidance", "Turns the analysis into a clear risk level and practical next step."),
]

for col, icon, title, text in features:
    with col:
        st.markdown(
            f'<div class="feature"><div class="feature-icon">{icon}</div>'
            f'<div class="feature-title">{title}</div>'
            f'<div class="feature-text">{text}</div></div>',
            unsafe_allow_html=True
        )

st.markdown(
    '<div class="footer">ScamShield AI • Machine Learning + Neural Network + Rule-Based Risk Analysis</div>',
    unsafe_allow_html=True
)