# AI Scam Detector

A Streamlit app that detects scam risk from uploaded screenshots or pasted text. The app uses OCR for images and can optionally call Gemini if a `GEMINI_API_KEY` is configured.

## Run locally

1. Create a virtual environment and install dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-lite.txt
```

2. Start the app:

```powershell
streamlit run app.py
```

## Environment

Create a `.env` file with the optional Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

If no key is set, the app will use a simple fallback analysis.

## Files

- `app.py` - Streamlit frontend and UI logic
- `utils.py` - OCR extraction and text cleanup
- `scam_detector.py` - risk analysis and Gemini fallback
- `prompt.py` - prompt builder for Gemini
- `requirements-lite.txt` - lightweight dependency list
- `test_analyze.py` - basic validation test
