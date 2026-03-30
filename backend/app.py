from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

# ---------- SYSTEM 1: AI → 3D PIPELINE ----------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("text", "")

    # Model selection (simple + reliable)
    if "helmet" in user_input.lower() or "hard hat" in user_input.lower():
        model_url = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
    elif "car" in user_input.lower():
        model_url = "https://modelviewer.dev/shared-assets/models/Car.glb"
    elif "robot" in user_input.lower():
        model_url = "https://modelviewer.dev/shared-assets/models/RobotExpressive.glb"
    else:
        model_url = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"

    # AI explanation
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an educational assistant."},
            {"role": "user", "content": f"Explain what a {user_input} is used for in 2 simple sentences."}
        ]
    )

    explanation = response.choices[0].message.content

    return jsonify({
        "model_url": model_url,
        "explanation": explanation
    })


# ---------- SYSTEM 2: AVATAR ----------
@app.route("/animate", methods=["POST"])
def animate():
    text = request.json.get("text", "")

    response = client.chat.completions.create(
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

    action = response.choices[0].message.content.strip().lower()

    explanation = f"The avatar performs: {action}"

    return jsonify({
        "action": action,
        "explanation": explanation
    })


if __name__ == "__main__":
    app.run(debug=True)
