import gradio as gr
import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


# ---------- AI TEXT ----------
def query_ai(prompt):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=30
        )
        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"]

        return f"AI error: {result}"

    except Exception as e:
        return f"Request failed: {str(e)}"


# ---------- MODEL MAP ----------
MODEL_MAP = {
    "helmet": "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
    "car": "https://modelviewer.dev/shared-assets/models/Car.glb",
    "robot": "https://modelviewer.dev/shared-assets/models/RobotExpressive.glb",
    "duck": "https://modelviewer.dev/shared-assets/models/Duck.glb",
    "fox": "https://modelviewer.dev/shared-assets/models/Fox.glb"
}


def get_model(text):
    text = text.lower()
    for key in MODEL_MAP:
        if key in text:
            return MODEL_MAP[key]
    return MODEL_MAP["robot"]


# ---------- SYSTEM 1 ----------
def generate_object(text):

    if not text:
        return "Enter an object.", "", ""

    explanation = query_ai(
        f"Explain what a {text} is used for in two simple sentences."
    )

    model_url = get_model(text)

    viewer_html = f"""
    <model-viewer src="{model_url}" auto-rotate camera-controls style="width:100%; height:400px;"></model-viewer>
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
    """

    return explanation, model_url, viewer_html


# ---------- SYSTEM 2 ----------
def control_avatar(command):

    if not command:
        return "Enter a command."

    result = query_ai(
        f"Choose one word: walk, wave, point, idle. Command: {command}"
    )

    action = result.lower()

    if "walk" in action:
        return "Avatar performs: walk"
    elif "wave" in action:
        return "Avatar performs: wave"
    elif "point" in action:
        return "Avatar performs: point"
    else:
        return "Avatar performs: idle"


# ---------- UI ----------
with gr.Blocks(title="AI 3D Learning") as app:

    gr.Markdown("# AI 3D Learning")

    with gr.Tab("3D Generator"):

        text_input = gr.Textbox(label="Enter object")
        btn = gr.Button("Generate")

        explanation = gr.Textbox(label="Explanation")
        model_url = gr.Textbox(label="Model URL")
        viewer = gr.HTML()

        btn.click(
            generate_object,
            inputs=text_input,
            outputs=[explanation, model_url, viewer]
        )

    with gr.Tab("Avatar"):

        cmd = gr.Textbox(label="Command")
        btn2 = gr.Button("Run")

        output = gr.Textbox(label="Result")

        btn2.click(
            control_avatar,
            inputs=cmd,
            outputs=output
        )


app.launch()
