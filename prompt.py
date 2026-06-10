# Prompt templates for Gemini
def build_prompt(text: str) -> str:
    return (
        "Analyze the following text for scam risk and return only valid JSON with these keys: "
        "risk_score, threat_level, scam_type, reasons, recommendations. "
        "Use integers for risk_score and arrays for reasons and recommendations.\n\n"
        f"Text:\n{text}\n\n"
        "Return output in this form exactly, without explanation:\n"
        "{\n"
        "  \"risk_score\": 0,\n"
        "  \"threat_level\": \"Low\",\n"
        "  \"scam_type\": \"Unknown\",\n"
        "  \"reasons\": [],\n"
        "  \"recommendations\": []\n"
        "}"
    )
