import os
from dotenv import load_dotenv
import streamlit as st
from io import BytesIO
from utils import extract_text_from_image, clean_text
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
            background: linear-gradient(135deg, #0f172a 0%, #0e7490 45%, #38bdf8 100%);
        }
        .block-container {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            padding: 2rem 2rem 2rem;
            box-shadow: 0 30px 80px rgba(15, 23, 42, 0.12);
            color: #0f172a;
        }
        /* Ensure text inside Streamlit containers is dark/readable */
        .block-container, .block-container * {
            color: #0f172a !important;
        }
        .app-title {
            font-size: 3.4rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0.2rem;
        }
        .app-subtitle {
            font-size: 1.05rem;
            color: #334155;
            margin-top: 0;
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            background-color: #0e7490;
            color: #ffffff !important;
            border: none;
            border-radius: 10px;
            padding: 0.85rem 1.3rem;
            font-weight: 700;
        }
        .stButton>button:hover {
            background-color: #075985;
            color: #ffffff !important;
        }
        .component-card {
            background: #f8fafc;
            border-radius: 20px;
            padding: 1.4rem;
            box-shadow: 0 18px 50px rgba(15, 23, 42, 0.06);
            color: #0f172a;
        }
        .component-card h3 {
            margin-bottom: 0.75rem;
            color: #0f172a;
        }
        /* Text area and upload widget readability */
        .stTextArea textarea, textarea, .stTextInput input {
            background-color: #ffffff !important;
            color: #0f172a !important;
        }
        .stFileUploader, .stFileUploader * {
            color: #0f172a !important;
            background-color: transparent !important;
        }
        /* Force uploader drop zone and uploaded file rows to be light and readable (broad selectors) */
        .stFileUploader div[role="button"], .stFileUploader [role="button"], .stFileUploader .upload, .stFileUploader .stFileUploader, .stFileUploader .css-1v3fvcr, .stFileUploader .css-1e5imcs, .stFileUploader .upload-button, .stFileUploader .UploadedFile, .stFileUploader .uploadedFile {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #e6eef7 !important;
            box-shadow: none !important;
        }
        .stFileUploader .stFileUploaderLabel, .stFileUploader .uploadedFile, .stFileUploader .css-1v3fvcr * {
            background-color: transparent !important;
            color: #0f172a !important;
        }
        /* Textarea border & background reset */
        .stTextArea textarea, textarea, .stTextInput input {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #d1d5db !important;
            border-radius: 6px !important;
        }
        /* Metrics and values */
        .stMetric, .stMetric-value, .stMetric-label, .stMetric > div {
            color: #0f172a !important;
        }
        /* Markdown content inside cards */
        .component-card p, .component-card li {
            color: #334155 !important;
        }
        hr { border-top: 1px solid #cbd5e1; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='app-title'>AI Scam Detector</div>", unsafe_allow_html=True)
st.markdown(
    "<p class='app-subtitle'>Upload a screenshot or paste a suspicious message to get an instant scam risk score and protection guidance.</p>",
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
            "<ul style='margin: 0; padding-left: 1.1rem; color: #334155;'>"
            "<li>Upload image or text content.</li>"
            "<li>OCR extracts text from images.</li>"
            "<li>AI evaluates risk, type, and mitigation.</li>"
            "</ul></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='component-card'><h3>Security tips</h3>"
            "<ul style='margin: 0; padding-left: 1.1rem; color: #334155;'>"
            "<li>Do not click unknown links.</li>"
            "<li>Never share OTP or password.</li>"
            "<li>Verify sender identity independently.</li>"
            "</ul></div>",
            unsafe_allow_html=True,
        )

if analyze_button:
    text = ""
    if uploaded is not None:
        bytes_data = uploaded.read()
        if uploaded.type and uploaded.type.startswith("image"):
            with st.spinner("Running OCR..."):
                text = extract_text_from_image(bytes_data)
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

        status_message = "Low risk detected." if isinstance(score, int) and score < 40 else (
            "Medium risk detected." if isinstance(score, int) and score < 70 else "High risk detected."
        )

        st.markdown("<hr style='margin: 2rem 0 1.5rem; border: none; border-top: 1px solid #cbd5e1;' />", unsafe_allow_html=True)
        st.subheader("Analysis Result")
        st.write(f"**{status_message}**")

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Risk Score", score)
        metric_col2.metric("Threat Level", threat)
        metric_col3.metric("Scam Type", scam_type)

        st.markdown("<div class='component-card'><h3>Why this looks suspicious</h3></div>", unsafe_allow_html=True)
        for r in reasons:
            st.write("-", r)

        st.markdown("<div class='component-card'><h3>What to do next</h3></div>", unsafe_allow_html=True)
        for r in recommendations:
            st.write("-", r)
