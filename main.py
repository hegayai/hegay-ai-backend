import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load API keys
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# ---------------------------
# ROOT ENDPOINT
# ---------------------------
@app.route("/")
def home():
    return jsonify({"message": "Hegay AI backend is running on Render."})

# ---------------------------
# TEXT GENERATION ENDPOINT
# ---------------------------
@app.route("/generate-text", methods=["POST"])
def generate_text():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Simple placeholder response (you can connect your model later)
    return jsonify({
        "response": f"You said: {prompt}. Text generation model will be added soon."
    })

# ---------------------------
# IMAGE GENERATION ENDPOINT (Stability.ai SD3)
# ---------------------------
@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json"
    }

    payload = {
        "prompt": prompt,
        "output_format": "png"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({
            "error": "Image generation failed",
            "details": response.text
        }), 500

    result = response.json()
    image_base64 = result.get("image")

    return jsonify({"image": image_base64})

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
