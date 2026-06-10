import os
from dotenv import load_dotenv
import streamlit as st
from utils import extract_text_from_image, clean_text, is_ocr_available
from scam_detector import analyze_text

load_dotenv()

st.set_page_config(
    page_title="AI Scam Detector",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #0b1220 0%, #102a54 45%, #1d4ed8 100%);
        }
        .block-container {
            background: rgba(15, 23, 42, 0.94);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 24px;
            padding: 2rem 2rem 2rem;
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.32);
            color: #e2e8f0;
        }
        .app-title {
            font-size: 3.4rem;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 0.2rem;
        }
        .app-subtitle {
            font-size: 1.05rem;
            color: #cbd5e1;
            margin-top: 0;
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            background-color: #2563eb;
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 0.85rem 1.3rem;
            font-weight: 700;
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.24);
        }
        .stButton>button:hover {
            background-color: #1d4ed8;
            color: #ffffff;
        }
        .stTextArea textarea,
        .stTextInput>div>input,
        .stFileUploader {
            background: #0f172a !important;
            color: #f8fafc !important;
            border: 1px solid rgba(148, 163, 184, 0.35) !important;
            border-radius: 14px !important;
        }
        .stTextArea textarea::placeholder,
        .stTextInput>div>input::placeholder {
            color: #94a3b8 !important;
        }
        .component-card {
            background: rgba(30, 58, 138, 0.98);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 20px;
            padding: 1.4rem;
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
            color: #eff6ff;
        }
        .component-card h3 {
            margin-bottom: 0.75rem;
            color: #ffffff;
        }
        .component-card ul {
            margin: 0;
            padding-left: 1.1rem;
            color: #cbd5e1;
        }
        .component-card li {
            color: #cbd5e1;
        }
        .result-block {
            background: linear-gradient(180deg, #1f3a8a 0%, #2563eb 100%);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 22px;
            padding: 1.6rem;
            margin-top: 1.5rem;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.24);
            color: #f8fafc;
        }
        .result-heading {
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
            color: #ffffff;
        }
        .status-msg {
            color: #dbeafe;
            margin-bottom: 1.2rem;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            text-align: center;
            color: #eff6ff;
            margin-bottom: 0.8rem;
        }
        .metric-title {
            color: #c7d2fe;
            font-size: 0.95rem;
            margin-bottom: 0.55rem;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
        }
        .result-list-card {
            background: rgba(30, 58, 138, 0.98);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 22px;
            padding: 1.4rem;
            margin-top: 1rem;
            color: #eff6ff;
        }
        .result-list-card h3 {
            margin-top: 0;
            margin-bottom: 0.8rem;
            color: #ffffff;
        }
        .result-list-card ul {
            margin: 0;
            padding-left: 1.1rem;
            color: #cbd5e1;
        }
        .result-list-card li {
            color: #cbd5e1;
            margin-bottom: 0.4rem;
        }
        .css-1kyxreq {
            color: #f8fafc;
        }
        .stMarkdown p,
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3 {
            color: #f8fafc;
        }
        .css-1kyxreq {
            color: #f8fafc;
        }
        .stMarkdown p,
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3 {
            color: #f8fafc;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='app-title'>AI Scam Detector</div>", unsafe_allow_html=True)
st.markdown(
    "<p class='app-subtitle'>Upload a screenshot or paste suspicious text to get an instant scam risk score, type, and safety guidance.</p>",
    unsafe_allow_html=True,
)

with st.container():
    left, right = st.columns([2, 1])
    with left:
        uploaded = st.file_uploader(
            "Upload screenshot or text file",
            type=["png", "jpg", "jpeg", "txt"],
            help="Upload a scam screenshot or text file for analysis.",
        )
        text_input = st.text_area(
            "Or paste text here",
            height=220,
            help="Paste the suspicious message content here.",
        )
        analyze_button = st.button("Analyze")
    with right:
        st.markdown(
            "<div class='component-card'><h3>How it works</h3>"
            "<ul style='margin: 0; padding-left: 1.1rem; color: #cbd5e1;'>"
            "<li>Upload image or text content.</li>"
            "<li>OCR extracts text from images.</li>"
            "<li>AI evaluates risk, type, and mitigation.</li>"
            "</ul></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='component-card'><h3>Security tips</h3>"
            "<ul style='margin: 0; padding-left: 1.1rem; color: #cbd5e1;'>"
            "<li>Do not click unknown links.</li>"
            "<li>Never share OTP or passwords.</li>"
            "<li>Verify sender identity independently.</li>"
            "</ul></div>",
            unsafe_allow_html=True,
        )

if analyze_button:
    text = ""
    if uploaded is not None:
        bytes_data = uploaded.read()
        is_image = False
        if uploaded.type and uploaded.type.startswith("image"):
            is_image = True
        elif uploaded.name.lower().endswith((".png", ".jpg", ".jpeg")):
            is_image = True

        if is_image:
            if not is_ocr_available():
                st.warning("OCR support is not installed. Install easyocr and restart the app, or paste the text manually.")
            else:
                with st.spinner("Running OCR..."):
                    text = extract_text_from_image(bytes_data)
                if not text:
                    st.warning("Could not extract text from the uploaded image. Please try a clearer screenshot or paste the content directly.")
        else:
            try:
                text = bytes_data.decode("utf-8")
            except Exception:
                text = ""

    if not text:
        text = text_input

    text = clean_text(text or "")
    if not text.strip():
        st.error("Please provide a screenshot or text to analyze.")
    else:
        with st.spinner("Analyzing with AI..."):
            result = analyze_text(text)

        score = result.get("risk_score", "N/A")
        threat = result.get("threat_level", "N/A")
        scam_type = result.get("scam_type", "N/A")
        reasons = result.get("reasons", [])
        recommendations = result.get("recommendations", [])

        status_message = (
            "Low risk detected." if isinstance(score, int) and score < 40 else
            "Medium risk detected." if isinstance(score, int) and score < 70 else
            "High risk detected."
        )

        st.markdown(
            f"<div class='result-block'><div class='result-heading'>Analysis Result</div>"
            f"<div class='status-msg'>{status_message}</div></div>",
            unsafe_allow_html=True,
        )

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.markdown(
            f"<div class='metric-card'><div class='metric-title'>Risk Score</div>"
            f"<div class='metric-value'>{score}</div></div>",
            unsafe_allow_html=True,
        )
        metric_col2.markdown(
            f"<div class='metric-card'><div class='metric-title'>Threat Level</div>"
            f"<div class='metric-value'>{threat}</div></div>",
            unsafe_allow_html=True,
        )
        metric_col3.markdown(
            f"<div class='metric-card'><div class='metric-title'>Scam Type</div>"
            f"<div class='metric-value'>{scam_type}</div></div>",
            unsafe_allow_html=True,
        )

        if reasons:
            reasons_html = "<div class='result-list-card'><h3>Why this looks suspicious</h3><ul>"
            for r in reasons:
                reasons_html += f"<li>{r}</li>"
            reasons_html += "</ul></div>"
            st.markdown(reasons_html, unsafe_allow_html=True)

        if recommendations:
            recommendations_html = "<div class='result-list-card'><h3>What to do next</h3><ul>"
            for r in recommendations:
                recommendations_html += f"<li>{r}</li>"
            recommendations_html += "</ul></div>"
            st.markdown(recommendations_html, unsafe_allow_html=True)
