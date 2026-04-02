from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔐 USE ENV VARIABLE (DO NOT HARDCODE KEY IN GITHUB)
HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}


# ---------- HELPER FUNCTION ----------
def query_huggingface(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ---------- TEST 1: AI → 3D PIPELINE ----------
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No input text provided"}), 400

        # Placeholder 3D model (can upgrade later)
        model_url = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"

        payload = {
            "inputs": f"Question: What is a {text} used for? Answer in 2 simple sentences."
        }

        result = query_huggingface(payload)

        if isinstance(result, list) and "generated_text" in result[0]:
            explanation = result[0]["generated_text"]
        else:
            explanation = f"A {text} is commonly used for practical purposes."

        return jsonify({
            "model_url": model_url,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- TEST 2: AVATAR ----------
@app.route("/animate", methods=["POST"])
def animate():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No command provided"}), 400

        payload = {
            "inputs": f"Instruction: Choose one word (walk, wave, point, idle). Input: {text}. Output:"
        }

        result = query_huggingface(payload)

        if isinstance(result, list) and "generated_text" in result[0]:
            action_raw = result[0]["generated_text"].lower()

            # Clean mapping
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

        return jsonify({
            "action": action,
            "explanation": f"The avatar performs: {action}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- HEALTH CHECK ----------
@app.route("/")
def home():
    return jsonify({"status": "API running"})


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
