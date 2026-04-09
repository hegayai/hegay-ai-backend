from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.get("/")
def get_root():
    return "Hegay AI backend is running on Render."

# TEXT GENERATION
@app.post("/generate-text")
def post_generate_text():
    data = request.get_json()
    prompt = data.get("prompt") if data else None

    if not prompt:
        return jsonify({"error": "Missing 'prompt'"}), 400

    response = f"You said: {prompt}"
    return jsonify({"response": response})

# IMAGE GENERATION (HuggingFace SD 1.5)
@app.post("/generate-image")
def post_generate_image():
    data = request.get_json()
    prompt = data.get("prompt") if data else None

    if not prompt:
        return jsonify({"error": "Missing 'prompt'"}), 400

    HF_TOKEN = os.getenv("HF_TOKEN")
    if not HF_TOKEN:
        return jsonify({"error": "HF_TOKEN not set"}), 500

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-1-5",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt},
        )

        if response.status_code != 200:
            return jsonify({"error": "Image generation failed", "details": response.text}), 500

        return response.content, 200, {"Content-Type": "image/png"}

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
