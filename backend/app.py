from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)
CORS(app)


# ---------- SYSTEM 1: AI → 3D PIPELINE ----------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("text", "")

    sketchfab_key = os.getenv("SKETCHFAB_API_KEY")

    # 🔍 Search Sketchfab
    search_url = "https://api.sketchfab.com/v3/search"
    params = {
        "q": user_input,
        "type": "models",
        "downloadable": "true",
        "staffpicked": "true"
    }

    headers = {
        "Authorization": f"Token {sketchfab_key}"
    }

    try:
        res = requests.get(search_url, headers=headers, params=params)
        results = res.json()

        sketchfab_name = results["results"][0]["name"]
    except:
        sketchfab_name = "No result found"

    # 🎯 GLB fallback mapping (for Three.js compatibility)
    if "helmet" in user_input.lower() or "hard hat" in user_input.lower():
        model_url = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
    elif "car" in user_input.lower():
        model_url = "https://modelviewer.dev/shared-assets/models/Car.glb"
    elif "robot" in user_input.lower():
        model_url = "https://modelviewer.dev/shared-assets/models/RobotExpressive.glb"
    else:
        model_url = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"

    # 🤖 AI Explanation
    ai_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an educational assistant."},
            {"role": "user", "content": f"Explain what a {user_input} is used for in 2 simple sentences."}
        ]
    )

    explanation = ai_response.choices[0].message.content

    return jsonify({
        "model_url": model_url,
        "explanation": explanation,
        "sketchfab_result": sketchfab_name
    })


# ---------- SYSTEM 2: AVATAR ----------
@app.route("/animate", methods=["POST"])
def animate():
    text = request.json.get("text", "")

    ai_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Classify the user's command into one word: walk, wave, point, idle."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    action = ai_response.choices[0].message.content.strip().lower()

    explanation = f"The avatar performs: {action}"

    return jsonify({
        "action": action,
        "explanation": explanation
    })


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)
