import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# ---------------------------
# ROOT ENDPOINT
# ---------------------------
@app.route("/")
def home():
    return jsonify({"message": "Hegay AI backend is running successfully on Render."})

# ---------------------------
# TEXT GENERATION ENDPOINT
# ---------------------------
@app.route("/generate-text", methods=["POST"])
def generate_text():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    return jsonify({
        "response": f"You said: {prompt}. Text generation model will be added soon."
    })

# ---------------------------
# IMAGE GENERATION (Stability SD3 - multipart/form-data)
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

    # multipart/form-data payload
    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return jsonify({
            "error": "Image generation failed",
            "details": response.text
        }), 500

    result = response.json()
    image_base64 = result.get("image")

    return jsonify({"image": image_base64})

# ---------------------------
# IMAGE TEST PAGE
# ---------------------------
@app.route("/image-test")
def image_test():
    return """
    <html>
    <head>
        <title>Hegay AI Image Test</title>
    </head>
    <body style="font-family: Arial; padding: 40px;">
        <h2>Hegay AI – Image Generator Test</h2>
        <form onsubmit="generateImage(); return false;">
            <input id="prompt" type="text" placeholder="Enter prompt" style="width: 300px; padding: 8px;">
            <button type="submit" style="padding: 8px;">Generate</button>
        </form>
        <p id="status"></p>
        <img id="result" style="margin-top: 20px; max-width: 400px;">
        
        <script>
            async function generateImage() {
                document.getElementById("status").innerText = "Generating...";
                const prompt = document.getElementById("prompt").value;

                const response = await fetch('/generate-image', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt})
                });

                const data = await response.json();

                if (data.image) {
                    document.getElementById("result").src = "data:image/png;base64," + data.image;
                    document.getElementById("status").innerText = "Done.";
                } else {
                    document.getElementById("status").innerText = "Error: " + JSON.stringify(data);
                }
            }
        </script>
    </body>
    </html>
    """

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
