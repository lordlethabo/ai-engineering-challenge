from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- SYSTEM 1: AI → 3D PIPELINE ----------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("text", "").lower()

    # Predefined models (no API needed)
    if "helmet" in user_input or "hard hat" in user_input:
        model_url = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
        explanation = "A hard hat is used in construction to protect the head from falling objects."
    elif "car" in user_input:
        model_url = "https://modelviewer.dev/shared-assets/models/Car.glb"
        explanation = "Cars are used for transportation of people and goods."
    elif "robot" in user_input:
        model_url = "https://modelviewer.dev/shared-assets/models/RobotExpressive.glb"
        explanation = "Robots are programmable machines used to perform tasks automatically."
    else:
        model_url = "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
        explanation = f"{user_input.capitalize()} is commonly used in real-world applications."

    return jsonify({
        "model_url": model_url,
        "explanation": explanation
    })


# ---------- SYSTEM 2: AVATAR ----------
@app.route("/animate", methods=["POST"])
def animate():
    text = request.json.get("text", "").lower()

    if "walk" in text:
        action = "walk"
    elif "wave" in text:
        action = "wave"
    elif "point" in text:
        action = "point"
    elif "hello" in text:
        action = "wave"
    else:
        action = "idle"

    explanation = f"The avatar performs: {action}"

    return jsonify({
        "action": action,
        "explanation": explanation
    })


if __name__ == "__main__":
    app.run(debug=True)
