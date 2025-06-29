import streamlit as st
import json
import os
from gtts import gTTS
from io import BytesIO

# Load prescription rules from JSON
def load_rules(json_path):
    if not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
        st.error("The prescription rules file is missing or empty.")
        return []
    with open(json_path, "r") as f:
        return json.load(f)

rules = load_rules("data/prescriptions.json")

# Suggest prescription based on problem text
def suggest_prescription(problem_text):
    problem_text = problem_text.lower()
    for condition in rules:
        for keyword in condition["keywords"]:
            if keyword in problem_text:
                return {
                    "tablets": condition.get("tablets", []),
                    "syrups": condition.get("syrups", [])
                }
    return {"tablets": [], "syrups": []}

# Generate TTS audio from text
def text_to_audio(text):
    tts = gTTS(text)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

# Streamlit UI
st.set_page_config(page_title="Patient Prescription Manager", layout="centered")
st.title("💊 Patient Prescription Management App")

st.markdown("Please enter patient details and symptoms. The system will suggest possible medications.")

with st.form("patient_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Patient Name", "")
        age = st.number_input("🎂 Age", min_value=0, max_value=120, value=25)
        weight = st.number_input("⚖️ Weight (kg)", min_value=1.0, max_value=200.0, value=70.0)

    with col2:
        bp = st.text_input("🩺 Blood Pressure (e.g., 120/80)")
        sugar = st.text_input("🩸 Sugar Level (e.g., 110 mg/dL)")

    problem = st.text_area("📝 Patient Problem (Symptoms)", "")

    submitted = st.form_submit_button("Get Prescription")

if submitted:
    if not name or not problem:
        st.warning("Please enter both name and symptoms.")
    else:
        prescription = suggest_prescription(problem)
        st.subheader(f"📋 Prescription for {name}")
        st.write(f"*Age:* {age} | *Weight:* {weight}kg | *BP:* {bp} | *Sugar:* {sugar}")
        
        text_output = f"Prescription for {name}. Age {age}, Weight {weight} kilograms. Blood pressure is {bp}, and sugar level is {sugar}.\n"

        st.markdown("### 💊 Tablets Prescribed:")
        if prescription["tablets"]:
            for tab in prescription["tablets"]:
                st.write(f"• {tab}")
            text_output += "Tablets prescribed: " + ", ".join(prescription["tablets"]) + ". "
        else:
            st.write("No specific tablets suggested.")
            text_output += "No specific tablets suggested. "

        st.markdown("### 🧴 Syrups Prescribed:")
        if prescription["syrups"]:
            for syp in prescription["syrups"]:
                st.write(f"• {syp}")
            text_output += "Syrups prescribed: " + ", ".join(prescription["syrups"]) + "."
        else:
            st.write("No specific syrups suggested.")
            text_output += "No specific syrups suggested."

        # Generate and play audio
        audio_bytes = text_to_audio(text_output)
        st.audio(audio_bytes, format="audio/mp3")