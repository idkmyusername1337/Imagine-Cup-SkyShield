import os
import streamlit as st
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
# SDK 4.0 Imports
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
import plotly.graph_objects as go

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

TEXT_ANALYTICS_ENDPOINT = os.getenv("TEXT_ANALYTICS_ENDPOINT")
TEXT_ANALYTICS_KEY = os.getenv("TEXT_ANALYTICS_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
VISION_ENDPOINT = os.getenv("VISION_ENDPOINT")
VISION_KEY = os.getenv("VISION_KEY")

# Validate credentials
missing_creds = [svc for svc, cred in [
    ("Text Analytics", TEXT_ANALYTICS_ENDPOINT and TEXT_ANALYTICS_KEY),
    ("Translator", TRANSLATOR_ENDPOINT and TRANSLATOR_KEY),
    ("Vision", VISION_ENDPOINT and VISION_KEY)
] if not cred]

if missing_creds:
    st.error(f"Missing Azure credentials: {', '.join(missing_creds)}. Check your .env file.")
    st.stop()

# --------------------------------------------------
# Initialize Azure clients
# --------------------------------------------------
text_client = TextAnalyticsClient(
    endpoint=TEXT_ANALYTICS_ENDPOINT,
    credential=AzureKeyCredential(TEXT_ANALYTICS_KEY)
)

translator_client = TextTranslationClient(
    endpoint=TRANSLATOR_ENDPOINT,
    credential=AzureKeyCredential(TRANSLATOR_KEY)
)

vision_client = ImageAnalysisClient(
    endpoint=VISION_ENDPOINT,
    credential=AzureKeyCredential(VISION_KEY)
)

# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def analyze_image_text(image_data):
    """Extracts text from images to identify security alerts using READ feature."""
    try:
        # FIX: Changed VisualFeatures.TEXT to VisualFeatures.READ for SDK 4.0
        result = vision_client.analyze(
            image_data=image_data,
            visual_features=[VisualFeatures.READ]
        )
        
        # FIX: Access the result using the .read property instead of .text
        if result.read is not None:
            extracted_lines = []
            for block in result.read.blocks:
                for line in block.lines:
                    extracted_lines.append(line.text)
            return " ".join(extracted_lines)
        return ""
    except Exception as e:
        st.error(f"Vision Analysis Error: {str(e)}")
        return ""

def translate_alert(text: str, language: str) -> str:
    lang_map = {"English": "en", "Spanish": "es", "French": "fr", "German": "de"}
    if language == "None" or language not in lang_map:
        return text

    try:
        response = translator_client.translate(
            body=[text], 
            to_language=[lang_map[language]]
        )
        return response[0].translations[0].text
    except Exception as e:
        st.error(f"Translation Error: {str(e)}")
        return text

def analyze_text(text: str) -> (str, list, int):
    response = text_client.extract_key_phrases(documents=[text])[0]
    key_phrases = response.key_phrases if not response.is_error else []

    risk_score = 0
    lower_text = text.lower()
    if any(word in lower_text for word in ["high", "critical"]): risk_score += 5
    if any(word in lower_text for word in ["malware", "compromised", "unauthorized", "brute force"]): risk_score += 3
    risk_score = min(risk_score, 10)

    explanation = f"""
### 🔍 Alert Analysis
**Key Indicators Detected:** {', '.join(key_phrases) if key_phrases else 'None'}
**Summary:** This activity reflects common attack patterns and requires immediate triage.
"""
    return explanation, key_phrases, risk_score

def risk_score_chart(score: int):
    # Your original Gauge Chart logic
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "red" if score >= 7 else "orange" if score >= 4 else "green"},
            'steps': [{'range': [0, 4], 'color': 'lightgray'}, {'range': [4, 7], 'color': 'gray'}]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
st.set_page_config(page_title="🛡️ SKYSHIELD", layout="wide")
st.markdown("<h1 style='text-align:center;'>🛡️ SKYSHIELD</h1>", unsafe_allow_html=True)
st.divider()

col_input, col_viz = st.columns([1, 1])

with col_input:
    uploaded_image = st.file_uploader("Upload Security Alert Image", type=["jpg", "jpeg", "png"])
    
    initial_text = ""
    if uploaded_image:
        with st.spinner("Reading image..."):
            initial_text = analyze_image_text(uploaded_image.getvalue())
    
    # Text area reflects extracted or manual text
    alert_text = st.text_area("Security Alert Text", value=initial_text, height=200)
    target_lang = st.selectbox("Translate To", ["None", "English", "Spanish", "French", "German"])
    analyze = st.button("🔍 Analyze Alert", use_container_width=True)

if analyze and alert_text.strip():
    translated_text = translate_alert(alert_text, target_lang)
    explanation, key_phrases, risk_score = analyze_text(translated_text)

    with col_viz:
        # Your original chart renders here
        risk_score_chart(risk_score)
        st.markdown(f"**Severity:** {'🔴 High' if risk_score >= 7 else '🟠 Medium' if risk_score >= 4 else '🟢 Low'}")
    
    st.divider()
    st.markdown(explanation)
    if target_lang != "None":
        with st.expander("🌐 See Translated Content"):
            st.write(translated_text)
