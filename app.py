import os
from dotenv import load_dotenv
import streamlit as st
from utils import extract_text_from_image, clean_text
from scam_detector import analyze_text

load_dotenv()

# =========================
# LANGUAGE SUPPORT
# =========================

LANG = {
    "English": {
        "page_title": "AI Scam Detector Pro",
        "title": "🛡️ AI Scam Detector",
        "subtitle": "Detect phishing, fraud, impersonation and malicious messages using AI-powered analysis.",
        "language": "🌐 Language",
        "upload": "Upload Screenshot / Text File",
        "paste": "Paste suspicious content",
        "analyze": "Analyze Message",
        "result": "Analysis Result",
        "risk": "Risk Score",
        "threat": "Threat Level",
        "type": "Scam Type",
        "why": "Why It Looks Suspicious",
        "next": "Recommended Actions",
        "pipeline_title": "Detection Pipeline",
        "pipeline_steps": [
            "Upload screenshot or text",
            "OCR extracts content",
            "Gemini AI analyzes risk",
            "Security recommendations generated",
        ],
        "tips_title": "Safety Tips",
        "tips": [
            "Never share OTPs",
            "Verify sender identity",
            "Avoid unknown links",
            "Do not download suspicious files",
        ],
        "ocr_spinner": "Running OCR...",
        "analysis_spinner": "Analyzing with AI...",
        "empty_error": "Please provide text or an image.",
        "high_risk": "HIGH RISK DETECTED",
        "medium_risk": "MEDIUM RISK DETECTED",
        "low_risk": "LOW RISK DETECTED",
        "extracted": "Extracted Content",
        "threat_levels": {
            "Low": "Low",
            "Medium": "Medium",
            "High": "High",
            "Unknown": "Unknown",
        },
        "scam_types": {
            "Phishing": "Phishing",
            "Unknown": "Unknown",
        },
        "fallback_reason": "No obvious indicators found.",
        "parse_error": "Model returned unparsable response."
    },

    "తెలుగు": {
        "page_title": "AI మోసాల గుర్తింపు ప్రో",
        "title": "🛡️ AI మోసాల గుర్తింపు వ్యవస్థ",
        "subtitle": "AI ఆధారిత విశ్లేషణతో మోసపూరిత సందేశాలను గుర్తించండి.",
        "language": "🌐 భాష",
        "upload": "స్క్రీన్‌షాట్ లేదా ఫైల్ అప్లోడ్ చేయండి",
        "paste": "సందేశాన్ని పేస్ట్ చేయండి",
        "analyze": "విశ్లేషించండి",
        "result": "విశ్లేషణ ఫలితం",
        "risk": "ప్రమాద స్కోర్",
        "threat": "ప్రమాద స్థాయి",
        "type": "మోసం రకం",
        "why": "ఎందుకు అనుమానాస్పదంగా ఉంది",
        "next": "తదుపరి చర్యలు",
        "pipeline_title": "గుర్తింపు ప్రక్రియ",
        "pipeline_steps": [
            "స్క్రీన్‌షాట్ లేదా టెక్స్ట్ అప్లోడ్ చేయండి",
            "OCR కంటెంట్‌ను వెలికితీస్తుంది",
            "Gemini AI ప్రమాదాన్ని విశ్లేషిస్తుంది",
            "భద్రతా సూచనలు రూపొందించబడతాయి",
        ],
        "tips_title": "భద్రతా చిట్కాలు",
        "tips": [
            "OTPలను ఎప్పుడూ పంచుకోవద్దు",
            "పంపిన వ్యక్తి గుర్తింపును ధృవీకరించండి",
            "తెలియని లింకులను నివారించండి",
            "అనుమానాస్పద ఫైళ్లను డౌన్‌లోడ్ చేయవద్దు",
        ],
        "ocr_spinner": "OCR నడుస్తోంది...",
        "analysis_spinner": "AIతో విశ్లేషిస్తోంది...",
        "empty_error": "దయచేసి టెక్స్ట్ లేదా చిత్రాన్ని అందించండి.",
        "high_risk": "అధిక ప్రమాదం గుర్తించబడింది",
        "medium_risk": "మధ్యస్థ ప్రమాదం గుర్తించబడింది",
        "low_risk": "తక్కువ ప్రమాదం గుర్తించబడింది",
        "extracted": "వెలికితీసిన కంటెంట్",
        "threat_levels": {
            "Low": "తక్కువ",
            "Medium": "మధ్యస్థం",
            "High": "అధికం",
            "Unknown": "తెలియదు",
        },
        "scam_types": {
            "Phishing": "ఫిషింగ్",
            "Unknown": "తెలియదు",
        },
        "fallback_reason": "స్పష్టమైన సూచనలు కనబడలేదు.",
        "parse_error": "మోడల్ అర్థం చేసుకోలేని ప్రతిస్పందనను ఇచ్చింది."
    },

    "हिन्दी": {
        "page_title": "AI स्कैम डिटेक्टर प्रो",
        "title": "🛡️ AI स्कैम डिटेक्टर",
        "subtitle": "AI आधारित विश्लेषण द्वारा संदिग्ध संदेशों की पहचान करें।",
        "language": "🌐 भाषा",
        "upload": "स्क्रीनशॉट या फ़ाइल अपलोड करें",
        "paste": "संदेश पेस्ट करें",
        "analyze": "विश्लेषण करें",
        "result": "विश्लेषण परिणाम",
        "risk": "जोखिम स्कोर",
        "threat": "खतरे का स्तर",
        "type": "स्कैम प्रकार",
        "why": "यह संदिग्ध क्यों है",
        "next": "अगले कदम",
        "pipeline_title": "पहचान प्रक्रिया",
        "pipeline_steps": [
            "स्क्रीनशॉट या टेक्स्ट अपलोड करें",
            "OCR सामग्री निकालता है",
            "Gemini AI जोखिम का विश्लेषण करता है",
            "सुरक्षा सुझाव तैयार होते हैं",
        ],
        "tips_title": "सुरक्षा सुझाव",
        "tips": [
            "OTP कभी साझा न करें",
            "भेजने वाले की पहचान सत्यापित करें",
            "अनजान लिंक से बचें",
            "संदिग्ध फ़ाइलें डाउनलोड न करें",
        ],
        "ocr_spinner": "OCR चल रहा है...",
        "analysis_spinner": "AI से विश्लेषण हो रहा है...",
        "empty_error": "कृपया टेक्स्ट या छवि दें।",
        "high_risk": "उच्च जोखिम मिला",
        "medium_risk": "मध्यम जोखिम मिला",
        "low_risk": "कम जोखिम मिला",
        "extracted": "निकाली गई सामग्री",
        "threat_levels": {
            "Low": "कम",
            "Medium": "मध्यम",
            "High": "उच्च",
            "Unknown": "अज्ञात",
        },
        "scam_types": {
            "Phishing": "फ़िशिंग",
            "Unknown": "अज्ञात",
        },
        "fallback_reason": "कोई स्पष्ट संकेत नहीं मिला।",
        "parse_error": "मॉडल ने पढ़ने योग्य प्रतिक्रिया नहीं दी।"
    }
}

language_options = ["English", "తెలుగు", "हिन्दी"]
current_lang = st.session_state.get("selected_lang", "English")
current_lang = current_lang if current_lang in language_options else "English"

st.set_page_config(
    page_title=LANG[current_lang]["page_title"],
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

selected_lang = st.sidebar.selectbox(
    LANG[current_lang]["language"],
    language_options,
    index=language_options.index(current_lang),
    key="selected_lang",
)

T = LANG[selected_lang]

# =========================
# CSS
# =========================

st.markdown("""
<style>
:root{
    --ink:#0f172a;
    --muted:#475569;
    --soft:#64748b;
    --line:#dbe3ef;
    --card:#ffffff;
    --brand:#0f766e;
    --brand-dark:#115e59;
    --accent:#2563eb;
}

.stApp{
    background:linear-gradient(180deg,#f8fafc 0%,#eef6f8 48%,#f8fafc 100%);
    color:var(--ink);
}

.main .block-container{
    padding-top:1.75rem;
    padding-bottom:3rem;
    max-width:1180px;
}

h1,h2,h3,h4,h5,h6,p,li,label,
[data-testid="stMarkdownContainer"]{
    color:var(--ink);
}

[data-testid="stSidebar"]{
    background:#ffffff;
    border-right:1px solid var(--line);
}

[data-testid="stSidebar"] *{
    color:var(--ink) !important;
}

.hero-card{
    background:linear-gradient(135deg,#0f172a 0%,#134e4a 58%,#0e7490 100%);
    padding:34px 36px;
    border-radius:26px;
    border:1px solid rgba(255,255,255,0.14);
    box-shadow:0 22px 55px rgba(15,23,42,.22);
    margin-bottom:24px;
}

.hero-title{
    color:#ffffff;
    font-size:clamp(2.1rem,4vw,3.4rem);
    font-weight:800;
    letter-spacing:-0.045em;
    line-height:1.05;
    margin-bottom:12px;
}

.hero-subtitle{
    color:#d9f3f0;
    font-size:clamp(1rem,1.7vw,1.18rem);
    line-height:1.65;
    max-width:780px;
}

.glass{
    background:var(--card);
    padding:26px;
    border-radius:22px;
    border:1px solid var(--line);
    box-shadow:0 16px 42px rgba(15,23,42,.08);
}

.glass h3{
    margin:0 0 16px 0;
    font-size:1.22rem;
    line-height:1.3;
    font-weight:750;
    letter-spacing:-0.02em;
    color:var(--ink);
}

.glass ul{
    margin:0;
    padding-left:1.15rem;
}

.glass li{
    color:var(--muted);
    line-height:1.65;
}

.feature-box{
    background:#f8fafc;
    padding:14px 16px;
    border-radius:14px;
    margin-bottom:12px;
    border:1px solid #e2e8f0;
    border-left:4px solid var(--brand);
    color:var(--muted);
    font-size:.98rem;
    line-height:1.45;
}

.risk-high,
.risk-medium,
.risk-low{
    padding:14px 16px;
    border-radius:14px;
    font-size:1rem;
    font-weight:800;
    letter-spacing:.01em;
    border:1px solid transparent;
    margin:14px 0 8px;
}

.risk-high{
    background:#fef2f2;
    border-color:#fecaca;
    color:#991b1b;
}

.risk-medium{
    background:#fffbeb;
    border-color:#fde68a;
    color:#92400e;
}

.risk-low{
    background:#ecfdf5;
    border-color:#bbf7d0;
    color:#166534;
}

.stTextArea label,
.stFileUploader label{
    color:var(--ink) !important;
    font-size:1rem !important;
    font-weight:700 !important;
}

.stTextArea textarea{
    background:#ffffff !important;
    color:var(--ink) !important;
    border:1px solid #cbd5e1 !important;
    border-radius:14px !important;
    font-size:1rem !important;
    line-height:1.55 !important;
}

.stFileUploader section{
    background:#f8fafc !important;
    border:1px dashed #94a3b8 !important;
    border-radius:16px !important;
}

.stFileUploader *{
    color:var(--ink) !important;
}

.stButton button{
    width:100%;
    min-height:54px;
    font-size:1.02rem;
    font-weight:800;
    border-radius:14px;
    background:linear-gradient(90deg,var(--brand-dark),var(--accent));
    color:#ffffff !important;
    border:none;
    box-shadow:0 12px 28px rgba(37,99,235,.22);
}

.stButton button:hover{
    filter:brightness(1.04);
    box-shadow:0 14px 32px rgba(37,99,235,.28);
}

[data-testid="stMetric"]{
    background:#ffffff;
    border:1px solid var(--line);
    border-radius:18px;
    padding:18px 20px;
    box-shadow:0 12px 30px rgba(15,23,42,.07);
}

[data-testid="stMetricValue"]{
    color:var(--ink) !important;
    font-size:clamp(1.45rem,2.4vw,2.05rem) !important;
    font-weight:850 !important;
    letter-spacing:-0.035em;
}

[data-testid="stMetricLabel"]{
    color:var(--soft) !important;
    font-size:.9rem !important;
    font-weight:700 !important;
}

[data-testid="stExpander"]{
    background:#ffffff;
    border:1px solid var(--line);
    border-radius:16px;
}

.stAlert{
    color:var(--ink) !important;
}

@media (max-width: 768px){
    .main .block-container{
        padding-left:1rem;
        padding-right:1rem;
    }

    .hero-card,
    .glass{
        padding:22px;
        border-radius:20px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================

st.markdown(f"""
<div class="hero-card">
<div class="hero-title">{T['title']}</div>
<div class="hero-subtitle">
{T['subtitle']}
</div>
</div>
""", unsafe_allow_html=True)

# =========================
# MAIN UI
# =========================

left, right = st.columns([2.2,1])

with left:

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        f"📁 {T['upload']}",
        type=["png","jpg","jpeg","txt"]
    )

    text_input = st.text_area(
        f"✍️ {T['paste']}",
        height=220
    )

    analyze_btn = st.button(
        f"🔍 {T['analyze']}"
    )

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    pipeline_steps = "".join(
        f'<div class="feature-box">{i}. {step}</div>'
        for i, step in enumerate(T["pipeline_steps"], start=1)
    )

    st.markdown(f"""
    <div class="glass">
    <h3>⚡ {T['pipeline_title']}</h3>
    {pipeline_steps}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    safety_tips = "".join(f"<li>{tip}</li>" for tip in T["tips"])

    st.markdown(f"""
    <div class="glass">
    <h3>🔒 {T['tips_title']}</h3>
    <ul>
    {safety_tips}
    </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# ANALYSIS
# =========================

if analyze_btn:

    text = ""

    if uploaded is not None:

        data = uploaded.read()

        if uploaded.type and uploaded.type.startswith("image"):

            with st.spinner(T["ocr_spinner"]):
                text = extract_text_from_image(data)

        else:

            try:
                text = data.decode("utf-8")
            except:
                text = ""

    if not text:
        text = text_input

    text = clean_text(text)

    if not text.strip():

        st.error(T["empty_error"])
        st.stop()

    with st.spinner(T["analysis_spinner"]):
        result = analyze_text(text, selected_lang)

    score = result.get("risk_score", 0)
    threat = T["threat_levels"].get(result.get("threat_level", "Unknown"), result.get("threat_level", "Unknown"))
    scam_type = T["scam_types"].get(result.get("scam_type", "Unknown"), result.get("scam_type", "Unknown"))

    st.markdown(f"## 📊 {T['result']}")

    c1, c2, c3 = st.columns(3)

    c1.metric(T["risk"], score)
    c2.metric(T["threat"], threat)
    c3.metric(T["type"], scam_type)

    if isinstance(score, int):

        if score >= 70:
            st.markdown(
                f'<div class="risk-high">🚨 {T["high_risk"]}</div>',
                unsafe_allow_html=True
            )

        elif score >= 40:
            st.markdown(
                f'<div class="risk-medium">⚠️ {T["medium_risk"]}</div>',
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f'<div class="risk-low">✅ {T["low_risk"]}</div>',
                unsafe_allow_html=True
            )

    colA, colB = st.columns(2)

    with colA:

        st.subheader(f"🔎 {T['why']}")

        for item in result.get("reasons", []):
            st.write("•", item)

    with colB:

        st.subheader(f"🛡 {T['next']}")

        for item in result.get("recommendations", []):
            st.write("•", item)

    with st.expander(f"📄 {T['extracted']}"):
        st.write(text)
