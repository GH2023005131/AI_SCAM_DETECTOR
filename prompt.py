SYSTEM_PROMPT = """
You are a cybersecurity expert.

Analyze the given message and return ONLY valid JSON.

{
  "risk_score": 0-100,
  "threat_level": "Low/Medium/High",
  "scam_type": "Type of scam",
  "reasons": [],
  "warning_signs": [],
  "recommendations": []
}

Return no markdown.
Return only JSON.
"""

def build_prompt(text: str, language: str = "English") -> str:
    return f"""
{SYSTEM_PROMPT}

IMPORTANT:
Generate all text fields in {language} language.

Message:
{text}
"""