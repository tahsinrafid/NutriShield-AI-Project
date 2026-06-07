# 🥗 NutriShield AI — Instant Food Safety & Guidance

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://nutrishield-ai-project-rmefzpvbexn5jkftsmrts3.streamlit.app/)

⚡ Transform complex chemical labels into instant, actionable consumer safety verdicts.

NutriShield AI converts a photo of a packaged food label into two clear outputs: a consumer-friendly traffic-light safety verdict (Green / Amber / Red) and a clinician-grade technical deep-dive. Localized for Bangladesh, the app uses household measures and personalized health profiles to make guidance practical.

---

## ✨ Key Highlights

- **Traffic-Light Verdicts:** Immediate visual risk indicator (🔴 / 🟡 / 🟢).
- **Localized Guidance:** Serving advice in household measures (e.g., bati, muth, chamoch).
- **Personalized Analysis:** Factors age, weight, allergies, and chronic conditions.
- **Technical Deep-Dive:** Collapsible, evidence-backed breakdowns for professionals.
- **Demo Mode:** One-click sample product runs for presentations.

---

## 🛠️ Tech Stack

- Frontend: `Streamlit`
- AI: Google Gemini (configurable via environment variable)
- Images: `Pillow`
- Secrets: use environment variables or `st.secrets` (do not commit keys)

---

## Quickstart (local)

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Set your Gemini API key (preferred via environment variable):

```bash
# macOS / Linux
export GOOGLE_API_KEY="your_key_here"
# Windows (PowerShell - new shell)
setx GOOGLE_API_KEY "your_key_here"
```

Run the app:

```bash
streamlit run app.py
```

