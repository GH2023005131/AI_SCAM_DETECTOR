# Core scam risk analysis engine
import json
import os
from prompt import build_prompt

try:
    from google import genai
except ImportError:
    genai = None


def mock_analysis(text: str) -> dict:
    lowered = text.lower()
    score = 20
    reasons = []
    recommendations = []
    scam_type = "General scam"

    if "transfer" in lowered or "send" in lowered and "money" in lowered:
        score += 35
        reasons.append("The message requests money transfer or payment.")
        scam_type = "Payment scam"

    if "otp" in lowered or "one-time password" in lowered:
        score += 30
        reasons.append("It asks for OTP or sensitive verification codes.")
        scam_type = "Account takeover"

    if "click the link" in lowered or "verify your account" in lowered:
        score += 25
        reasons.append("It pushes urgent action and suspicious links.")
        scam_type = "Phishing"

    if "win" in lowered or "prize" in lowered or "congratulations" in lowered:
        score += 20
        reasons.append("It uses unexpected rewards to trick you.")
        scam_type = "Prize scam"

    if score < 40:
        threat_level = "Low"
    elif score < 70:
        threat_level = "Medium"
    else:
        threat_level = "High"

    if score >= 40:
        recommendations.append("Do not respond or click links in this message.")
        recommendations.append("Verify the sender through a trusted channel.")
        recommendations.append("Report it to your provider or security team.")
    else:
        recommendations.append("Keep this message under review and avoid sharing sensitive data.")

    return {
        "risk_score": min(score, 100),
        "threat_level": threat_level,
        "scam_type": scam_type,
        "reasons": reasons,
        "recommendations": recommendations,
    }


def analyze_text(text: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")

    if genai is not None and api_key:
        try:
            genai.configure(api_key=api_key)
            prompt = build_prompt(text)
            response = genai.generate_text(
                model="gemini-1.0",
                prompt=prompt,
            )
            raw = response.text if hasattr(response, "text") else str(response)
            parsed = json.loads(raw)
            return {
                "risk_score": parsed.get("risk_score", 0),
                "threat_level": parsed.get("threat_level", "Unknown"),
                "scam_type": parsed.get("scam_type", "Unknown"),
                "reasons": parsed.get("reasons", []),
                "recommendations": parsed.get("recommendations", []),
            }
        except Exception:
            return mock_analysis(text)

    return mock_analysis(text)
