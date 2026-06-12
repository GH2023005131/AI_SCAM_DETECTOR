# AI-Scam-Detector

Minimal MVP for detecting scams from pasted text or uploaded screenshots (OCR + AI analysis).

Quick start (Windows):

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Set your Gemini API key in `.env` as `GEMINI_API_KEY=` if integrating later.

Deployment notes
---------------

- The default `requirements.txt` includes OCR packages (`easyocr`, `torch`, `opencv-python`) which are large and may fail or be slow on hosted services. For lightweight deployment (Streamlit Cloud, Heroku free tier) use `requirements-lite.txt` which excludes heavy OCR packages.
- Options:
	- Use `requirements-lite.txt` and delegate OCR to a cloud provider (Google Vision API, AWS Textract) to avoid installing `torch`.
	- If you need on-host OCR, keep `easyocr` in `requirements.txt` but expect longer build times and larger slug sizes.
- Before deploying, set `GEMINI_API_KEY` as an environment variable in your host's dashboard (do not commit `.env`).

Quick deploy (lightweight):

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements-lite.txt
streamlit run app.py
```

