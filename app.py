import streamlit as st
from google import genai
from google.genai import types
import json

# 1. Page Configuration
st.set_page_config(
    page_title="AuraHealth Clinical Intake Core",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Injecting Custom CSS for Professional Dark Theme
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d1117 0%, #070a0e 100%);
        color: #f0f6fc;
    }
    .premium-title {
        background: linear-gradient(90deg, #4ade80, #3b82f6, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }
    .glass-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    .specialist-badge {
        background: linear-gradient(135deg, rgba(59,130,246,0.1) 0%, rgba(99,102,241,0.1) 100%);
        border: 1px solid #3b82f6;
        color: #60a5fa;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .condition-badge {
        background: linear-gradient(135deg, rgba(74,222,128,0.1) 0%, rgba(34,197,94,0.1) 100%);
        border: 1px solid #4ade80;
        color: #4ade80;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# 3. API Key Setup
# 3. API Key Setup
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# 4. Header Layout
st.markdown('<p class="premium-title">AURAHEALTH CLINICAL CORE</p>', unsafe_allow_html=True)
st.markdown("<p style='color: #8b949e; font-size: 1.05rem; margin-top:-10px;'>Predictive Diagnostic Triage & Specialist Routing Architecture</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: rgba(240,246,252,0.1); margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)
st.caption("CRITICAL NOTICE: This software functions strictly as an educational screening prototype. It does not replace formal clinical validation or professional medical consultation.")

# 5. Patient Profile Demographics Terminal
st.markdown("<h3 style='color:#fff; margin-bottom: 15px; margin-top: 20px;'>Patient Demographics Matrix</h3>", unsafe_allow_html=True)

col_p1, col_p2, col_p3, col_p4 = st.columns(4)
with col_p1:
    p_name = st.text_input("Patient Name / Identifier:", placeholder="e.g., Patient-01", key="input_name")
with col_p2:
    p_weight = st.number_input("Weight (kg):", min_value=1.0, max_value=500.0, value=70.0, step=0.1, key="input_weight")
with col_p3:
    p_age = st.number_input("Age (Years):", min_value=1, max_value=120, value=25, key="input_age")
with col_p4:
    p_gender = st.selectbox("Biological Sex Assignment:", ["Male", "Female", "Other"], key="input_gender")

# 6. User Symptom Input Block
st.markdown("<h3 style='color:#fff; margin-bottom: 15px; margin-top: 30px;'>Clinical Symptom Presentation</h3>", unsafe_allow_html=True)

user_symptoms = st.text_area(
    "Describe the physiological symptoms in detail:",
    placeholder="Describe the clinical manifestation, onset timeline, and localized area of discomfort...",
    key="input_symptoms",
    label_visibility="collapsed"
)

# Action Execution Button
st.markdown("<br>", unsafe_allow_html=True)
col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
with col_b2:
    analyze_btn = st.button("RUN DIAGNOSTIC ASSESSMENT", use_container_width=True, key="btn_run")

# 7. Deep Analytics Output Processing
if analyze_btn:
    if user_symptoms.strip() == "":
        st.toast("Input field null. Please provide clinical symptoms.")
    elif p_name.strip() == "":
        st.toast("Patient identifier missing. Form submission rejected.")
    else:
        with st.spinner("Processing clinical data strings and compiling pathology mapping..."):
            
            symptom_payload = (
                f"Patient Profile: Identifier={p_name}, Weight={p_weight}kg, Age={p_age} Years, Gender={p_gender}. "
                f"Symptom Manifestations: {user_symptoms}"
            )
            
            system_prompt = (
                "You are an advanced medical triage assistant. Analyze the user's demographic profile, weight metrics, and symptoms. "
                "Output a response strictly in structured JSON format. Do not write any conversational intro or outro text. "
                "The JSON must contain exactly these keys: "
                "'Disease', 'Description', 'Specialist', 'Underlying_Causes', 'Precautions', 'Medication'. "
                "For 'Precautions' and 'Medication', format them as a JSON array of strings. "
                "Ensure descriptions are clinically objective, formal, and free of conversational prose."
            )
            
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=symptom_payload,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        response_mime_type="application/json" 
                    )
                )
                
                medical_data = json.loads(response.text)
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown(f"#### Clinical Summary Report | Subject: {p_name} ({p_age} Years, {p_gender}, {p_weight} kg)")
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.markdown(f"""
                        <div class="glass-card" style="text-align: center;">
                            <span style="color:#8b949e; font-size:0.9rem; display:block; margin-bottom:8px;">PREDICTED PATHOLOGICAL PROFILE</span>
                            <span class="condition-badge">{medical_data.get('Disease', 'Undetermined Pathology')}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col_m2:
                    st.markdown(f"""
                        <div class="glass-card" style="text-align: center;">
                            <span style="color:#8b949e; font-size:0.9rem; display:block; margin-bottom:8px;">RECOMMENDED SPECIALIST ROUTING</span>
                            <span class="specialist-badge">{medical_data.get('Specialist', 'General Practitioner')}</span>
                        </div>
                    """, unsafe_allow_html=True)

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown(f"""
                        <div class="glass-card">
                            <h3 style="color:#60a5fa; margin-top:0;">Clinical Assessment Overview</h3>
                            <p style="color:#c9d1d9; line-height:1.6;">{medical_data.get('Description', 'Insufficient data.')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="glass-card">
                            <h3 style="color:#f43f5e; margin-top:0;">Biological Pathophysiology</h3>
                            <p style="color:#e2e8f0; background: rgba(244,63,94,0.03); padding: 15px; border-radius: 6px; border-left: 4px solid #f43f5e; line-height:1.6;">
                                {medical_data.get('Underlying_Causes', 'Insufficient data.')}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col_d2:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("<h3 style='color:#4ade80; margin-top:0;'>Triage Protocols & Mitigation Steps</h3>", unsafe_allow_html=True)
                    for p in medical_data.get('Precautions', []):
                        st.markdown(f"<div style='padding: 6px 0; color:#c9d1d9;'>- {p}</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("<h3 style='color:#fbbf24; margin-top:0;'>Correlated Reference Pharmacology</h3>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size:0.8rem; color:#8b949e; margin-top:-5px;'>Academic mapping reference only. Subject to specialist verification.</p>", unsafe_allow_html=True)
                    for m in medical_data.get('Medication', []):
                        st.markdown(f"<span style='background:rgba(251,191,36,0.08); border: 1px solid rgba(251,191,36,0.2); color:#fbbf24; padding:4px 10px; border-radius:4px; display:inline-block; margin: 4px; font-size:0.9rem;'>{m}</span>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"System Triage Interface Interrupted: {e}")