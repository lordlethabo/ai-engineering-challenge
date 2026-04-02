import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 🔑 Hugging Face API Key
HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# ---------- HELPER FUNCTION ----------
def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI 3D Learning System", layout="centered")

st.title("🤖 AI 3D Learning System")

# =========================
# TEST 1 — AI → 3D
# =========================
st.header("🔹 AI → 3D Object Generator")

text = st.text_input("Enter an object (helmet, car, robot)")

if st.button("Generate 3D + Explanation"):
    if text:
        payload = {
            "inputs": f"Question: What is a {text} used for? Answer in 2 simple sentences."
        }

        result = query_huggingface(payload)

        if isinstance(result, list) and "generated_text" in result[0]:
            explanation = result[0]["generated_text"]
        else:
            explanation = f"A {text} is commonly used in everyday life."

        st.success("Generated successfully!")

        st.write("### 📘 Explanation")
        st.write(explanation)

        # 3D model (iframe)
        model_url = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"

        st.write("### 🧊 3D Model Viewer")
        st.components.v1.html(f"""
        <model-viewer src="{model_url}" auto-rotate camera-controls style="width:100%; height:400px;"></model-viewer>
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
        """, height=420)

    else:
        st.warning("Please enter an object.")

# =========================
# TEST 2 — AVATAR
# =========================
st.header("🔹 AI Avatar Control")

command = st.text_input("Enter command (walk, wave, point)")

if st.button("Run Avatar Command"):
    if command:
        payload = {
            "inputs": f"Instruction: Choose one word (walk, wave, point, idle). Input: {command}. Output:"
        }

        result = query_huggingface(payload)

        if isinstance(result, list) and "generated_text" in result[0]:
            action_raw = result[0]["generated_text"].lower()

            if "walk" in action_raw:
                action = "walk"
            elif "wave" in action_raw:
                action = "wave"
            elif "point" in action_raw:
                action = "point"
            else:
                action = "idle"
        else:
            action = "idle"

        st.success(f"Avatar action: {action}")
        st.write(f"🧠 The avatar performs: {action}")

    else:
        st.warning("Enter a command.")
