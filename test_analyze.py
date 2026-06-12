import json
from scam_detector import analyze_text

sample = (
    "Urgent: Your bank account has suspicious activity. "
    "Click http://phish.example.com and verify your password immediately to avoid suspension. "
    "Call +1-555-123-4567 if you need help."
)
res = analyze_text(sample)
print(json.dumps(res, indent=2, ensure_ascii=False))
