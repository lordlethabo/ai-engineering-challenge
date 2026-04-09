import os
import uuid
import torch
import gradio as gr
import requests
from PIL import Image
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Loading Shap-E models...")

xm = load_model("transmitter", device=device)
model = load_model("text300M", device=device)
diffusion = diffusion_from_config(load_config("diffusion"))

print("Models loaded")

os.makedirs("generated_models", exist_ok=True)


def generate_explanation(text):

    payload = {
        "inputs": f"Explain what a {text} is used for in two simple sentences."
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"]

        return f"A {text} is commonly used in practical environments."

    except Exception as e:
        return f"Explanation generation error: {str(e)}"


def generate_3d_model(prompt):

    latents = sample_latents(
        batch_size=1,
        model=model,
        diffusion=diffusion,
        guidance_scale=15.0,
        model_kwargs=dict(texts=[prompt]),
        progress=True,
        clip_denoised=True,
        use_fp16=False,
        device=device,
    )

    mesh = decode_latent_mesh(xm, latents[0]).tri_mesh()

    file_name = f"generated_models/{uuid.uuid4()}.ply"
    mesh.write_ply(file_name)

    return file_name


def ai_3d_pipeline(text):

    if not text:
        return "Enter an object description.", "", ""

    explanation = generate_explanation(text)

    try:
        model_path = generate_3d_model(text)

        viewer_html = f"""
        <div>
        <p>Generated 3D mesh file:</p>
        <p>{model_path}</p>
        </div>
        """

        return explanation, model_path, viewer_html

    except Exception as e:
        return explanation, "", f"3D generation error: {str(e)}"


def interpret_avatar_command(command):

    payload = {
        "inputs": f"Choose one word from walk, wave, point, idle based on this instruction: {command}"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()

        if isinstance(result, list):
            action = result[0]["generated_text"].lower()

            if "walk" in action:
                return "Avatar action: walk"
            elif "wave" in action:
                return "Avatar action: wave"
            elif "point" in action:
                return "Avatar action: point"

        return "Avatar action: idle"

    except Exception as e:
        return f"Command interpretation error: {str(e)}"


with gr.Blocks(title="AI 3D Learning") as app:

    gr.Markdown("# AI 3D Learning")

    with gr.Tab("3D Object Generator"):

        text_input = gr.Textbox(
            label="Describe an object",
            placeholder="Example: construction helmet"
        )

        generate_btn = gr.Button("Generate 3D Object")

        explanation_output = gr.Textbox(label="Explanation")

        model_file_output = gr.Textbox(label="Generated Model File")

        viewer_output = gr.HTML(label="Viewer")

        generate_btn.click(
            ai_3d_pipeline,
            inputs=text_input,
            outputs=[explanation_output, model_file_output, viewer_output]
        )

    with gr.Tab("Avatar Command"):

        command_input = gr.Textbox(
            label="Enter command",
            placeholder="Example: wave hello to the learner"
        )

        avatar_btn = gr.Button("Run Command")

        avatar_output = gr.Textbox(label="Result")

        avatar_btn.click(
            interpret_avatar_command,
            inputs=command_input,
            outputs=avatar_output
        )

app.launch()
