import os
import json
from dotenv import load_dotenv
from prompt import build_prompt

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

FALLBACK_TEXT = {
    "English": {
        "no_indicators": "No obvious indicators found.",
        "parse_error": "Model returned unparsable response.",
    },
    "తెలుగు": {
        "no_indicators": "స్పష్టమైన సూచనలు కనబడలేదు.",
        "parse_error": "మోడల్ అర్థం చేసుకోలేని ప్రతిస్పందనను ఇచ్చింది.",
    },
    "हिन्दी": {
        "no_indicators": "कोई स्पष्ट संकेत नहीं मिला।",
        "parse_error": "मॉडल ने पढ़ने योग्य प्रतिक्रिया नहीं दी।",
    },
}


def mock_analysis(text, language="English"):
    fallback_text = FALLBACK_TEXT.get(language, FALLBACK_TEXT["English"])

    keywords = [
        "bank",
        "password",
        "urgent",
        "click",
        "verify",
        "transfer",
        "account",
        "ssn",
        "social",
        "login",
        "call",
        "limited time",
    ]

    score = 0
    reasons = []

    lower = text.lower()

    for k in keywords:
        if k in lower:
            score += 15

            if language == "తెలుగు":
                reasons.append(f"కీవర్డ్ గుర్తించబడింది: {k}")
            elif language == "हिन्दी":
                reasons.append(f"कीवर्ड मिला: {k}")
            else:
                reasons.append(f"Contains keyword: {k}")

    score = min(100, score)

    if score >= 60:
        level = "High"
    elif score >= 30:
        level = "Medium"
    else:
        level = "Low"

    scam_type = (
        "Phishing"
        if any(
            w in lower
            for w in ["bank", "password", "verify", "login", "account"]
        )
        else "Unknown"
    )

    if language == "తెలుగు":
        recommendations = [
            "లింకులను క్లిక్ చేయవద్దు.",
            "పంపిన వ్యక్తిని ధృవీకరించండి.",
            "మీ IT లేదా భద్రతా బృందానికి నివేదించండి."
        ]
    elif language == "हिन्दी":
        recommendations = [
            "लिंक पर क्लिक न करें।",
            "भेजने वाले की पहचान सत्यापित करें।",
            "अपनी IT टीम को रिपोर्ट करें।"
        ]
    else:
        recommendations = [
            "Do not click links or open attachments.",
            "Verify sender identity via known channels.",
            "Report to your IT/security team."
        ]

    return {
        "risk_score": score,
        "threat_level": level,
        "scam_type": scam_type,
        "reasons": reasons or [fallback_text["no_indicators"]],
        "recommendations": recommendations,
        "raw_text": text,
    }


def analyze_text(text, language="English"):
    fallback_text = FALLBACK_TEXT.get(language, FALLBACK_TEXT["English"])

    if not GEMINI_API_KEY:
        return mock_analysis(text, language)

    prompt = build_prompt(text, language)

    generated = None

    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        generated = response.text

    except Exception:
        generated = None

    if not generated:
        return mock_analysis(text, language)

    try:
        start = generated.find("{")
        end = generated.rfind("}") + 1

        if start >= 0 and end > start:
            generated = generated[start:end]

        return json.loads(generated)

    except Exception:
        return {
            "risk_score": None,
            "threat_level": "Unknown",
            "scam_type": "Unknown",
            "reasons": [fallback_text["parse_error"]],
            "recommendations": [],
            "raw_model_output": generated,
        }
