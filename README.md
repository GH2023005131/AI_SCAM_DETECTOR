# AI Scam Detector

AI Scam Detector is a Streamlit web app that helps identify suspicious or fraudulent messages from pasted text, uploaded text files, or screenshots. It uses OCR for images and AI-powered analysis to produce a risk score, threat level, scam type, suspicious indicators, and recommended safety actions.

## Features

- Analyze suspicious messages for scam risk.
- Upload screenshots or text files.
- Extract text from images using OCR.
- Generate AI-based scam analysis using Gemini when an API key is configured.
- Works with a local fallback analyzer when no Gemini API key is available.
- Supports multilingual UI and results in English, Telugu, and Hindi.
- Shows risk score, threat level, scam type, reasons, recommendations, and extracted content.

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- EasyOCR
- Pillow
- python-dotenv

## Project Structure

```text
AI_SCAM_DETECTOR/
├── app.py                 # Streamlit web app
├── scam_detector.py       # Scam analysis logic
├── prompt.py              # Gemini prompt builder
├── utils.py               # OCR and text utility functions
├── test_analyze.py        # Simple analyzer test script
├── requirements.txt       # Full dependencies with OCR support
├── requirements-lite.txt  # Lightweight dependencies for deployment
└── README.md
```

## Run Locally

1. Clone the repository:

```bash
git clone https://github.com/GH2023005131/AI_SCAM_DETECTOR.git
cd AI_SCAM_DETECTOR
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

The app still runs without this key by using the local fallback analyzer.

5. Start the app:

```bash
streamlit run app.py
```

## How To Use

1. Choose a language from the sidebar: English, Telugu, or Hindi.
2. Upload a screenshot or text file, or paste suspicious content into the text box.
3. Click `Analyze Message`.
4. Review the risk score, threat level, scam type, reasons, and recommended actions.

## Deployment Notes

The full `requirements.txt` includes OCR dependencies such as `easyocr` and `opencv-python`. These packages can be large and may slow down deployment on hosted platforms.

For lightweight deployment, use:

```bash
pip install -r requirements-lite.txt
```

If OCR is required in production, keep the full dependencies or use a cloud OCR service such as Google Vision API, AWS Textract, or Azure Computer Vision.

Before deploying, set `GEMINI_API_KEY` in your hosting provider's environment variables. Do not commit `.env` to Git.

## Example Output

The app returns:

- Risk Score: `0-100`
- Threat Level: `Low`, `Medium`, or `High`
- Scam Type: for example, `Phishing`
- Why it looks suspicious
- Recommended next steps
- Extracted content from uploaded files or screenshots

## Disclaimer

This tool is for awareness and educational use. It can help identify suspicious patterns, but it should not be treated as a final security decision. Always verify important messages through trusted official channels.
