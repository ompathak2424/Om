# निर्मोही निरञ्जन — Deployment Guide

## Deploy on Streamlit Community Cloud (Free)

### 1. Prepare GitHub Repository
Create a new public GitHub repository and upload these files:

```
astrology_app.py
requirements.txt
logo.png
.streamlit/config.toml
README.md
```

### 2. Deploy Steps
1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Select your repository
5. Set:
   - **Main file path:** `astrology_app.py`
   - **Python version:** 3.11 (or 3.10)
6. Click **Deploy**

### 3. After Deployment
- You will receive a public URL (e.g. `https://nirmohi-niranjan.streamlit.app`)
- Users can open it on any phone or computer
- On mobile, they can tap “Add to Home Screen” to use it like an app

## Local Testing Before Deploy
```bash
pip install -r requirements.txt
streamlit run astrology_app.py
```

## Notes
- The app uses Swiss Ephemeris for accurate calculations
- Internet is required only for place geocoding (Nominatim)
- All guidance is available in English, Hindi, and Gujarati
- Logo is included and displayed automatically
