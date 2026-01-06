
<img width="748" height="779" alt="SkyShield" src="https://github.com/user-attachments/assets/60714fae-634f-4611-afd9-a92e2448ce72" />

# 🛡️ SkyShield

**SkyShield** is an AI-powered security alert assistant built on **Microsoft Azure**.  
It helps security learners and junior researchers quickly understand, prioritize, and respond to security alerts using Azure AI services.

The project focuses on making enterprise-style security insights **accessible, explainable, and cost-effective**.

---

## 🚀 What SkyShield Does

SkyShield analyzes raw security alerts and provides:
- Clear explanations of what the alert means
- A calculated risk score to help prioritize incidents
- Multi-language translations for global accessibility
- Text extraction from image-based alerts (screenshots, photos)

---

## ✨ Key Features

### 🧠 Alert Understanding & Explanation
Uses **Azure AI Language (Text Analytics)** to extract key indicators and summarize alerts in human-readable form.

### 🚨 Risk Scoring & Prioritization
Assigns a severity score based on alert content to help identify high-risk incidents quickly.

### 🌍 Multi-Language Support
Translates security alerts into multiple languages using **Azure Translator**.

### 🖼️ Image-Based Alert Analysis
Extracts alert text from images using **Azure Computer Vision**, enabling analysis of screenshot-based alerts.

### 💸 Cost-Effective by Design
Built as a lightweight alternative to expensive enterprise security tools, ideal for students and early-career security professionals.

---

## 🛠️ Technology Stack

- **Python**
- **Streamlit**
- **Azure AI Language (Text Analytics)**
- **Azure Computer Vision**
- **Azure Translator**
- **Microsoft Azure**

---


---

## ⚙️ Setup & Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/skyshield.git
   cd skyshield
Create and activate a virtual environment

Install dependencies:

pip install -r requirements.txt

Create a .env file using .env.example and add your Azure credentials

Run the application:

streamlit run app.py

🎯 Use Cases

Security alert triage for SOC trainees

Learning security analysis and incident prioritization

Academic projects, demos, and research prototypes

🔮 Future Enhancements

Advanced risk scoring with visual dashboards

Incident timelines and alert correlation

Enhanced analytics and reporting

Improved image-based alert understanding

👤 Author

Built by a solo developer.



