from flask import Flask, request, jsonify, send_file
import requests
import os
from io import BytesIO

app = Flask(__name__)

# ============================
# ROOT ROUTE
# ============================
@app.get("/")
def get_root():
    return "Hegay AI backend is running on Render."


# ============================
# TEXT GENERATION ENDPOINT
# ============================
@app.post("/generate-text")
def generate_text():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = requests.post(
            "https://api.deepinfra.com/v1/openai/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('DEEPINFRA_API_KEY')}"},
            json={
                "model": "meta-llama/Llama-3.3-70B-Instruct",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200
            }
        )

        result = response.json()
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================
# IMAGE GENERATION ENDPOINT
# ============================
@app.post("/generate-image")
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = requests.post(
            "https://api.deepinfra.com/v1/inference/black-forest-labs/FLUX.1-dev",
            headers={"Authorization": f"Bearer {os.getenv('DEEPINFRA_API_KEY')}"},
            json={"prompt": prompt}
        )

        result = response.json()

        if "images" not in result:
            return jsonify({"error": "Image generation failed", "details": result}), 500

        image_url = result["images"][0]

        img_data = requests.get(image_url).content
        return send_file(BytesIO(img_data), mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================
# SIMPLE TEXT TEST PAGE (GET)
# ============================
@app.get("/text-test")
def text_test_page():
    return """
    <html>
        <body style="font-family: Arial; padding: 40px;">
            <h2>Hegay AI — Text Generation Test</h2>
            <form method="POST" onsubmit="event.preventDefault(); sendRequest();">
                <textarea id="prompt" rows="5" cols="50" placeholder="Enter your prompt here"></textarea><br><br>
                <button type="submit">Generate Text</button>
            </form>
            <h3>Response:</h3>
            <pre id="output"></pre>

            <script>
                async function sendRequest() {
                    const prompt = document.getElementById("prompt").value;
                    const response = await fetch("/generate-text", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({prompt})
                    });
                    const data = await response.json();
                    document.getElementById("output").innerText = JSON.stringify(data, null, 2);
                }
            </script>
        </body>
    </html>
    """


# ============================
# SIMPLE IMAGE TEST PAGE (GET)
# ============================
@app.get("/image-test")
def image_test_page():
    return """
    <html>
        <body style="font-family: Arial; padding: 40px;">
            <h2>Hegay AI — Image Generation Test</h2>
            <form method="POST" onsubmit="event.preventDefault(); sendImageRequest();">
                <textarea id="prompt" rows="5" cols="50" placeholder="Enter image prompt here"></textarea><br><br>
                <button type="submit">Generate Image</button>
            </form>
            <h3>Generated Image:</h3>
            <img id="result" style="max-width: 400px; display: none;" />
            <pre id="error"></pre>

            <script>
                async function sendImageRequest() {
                    const prompt = document.getElementById("prompt").value;
                    const response = await fetch("/generate-image", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({prompt})
                    });

                    if (response.headers.get("Content-Type").includes("image")) {
                        const blob = await response.blob();
                        const url = URL.createObjectURL(blob);
                        const img = document.getElementById("result");
                        img.src = url;
                        img.style.display = "block";
                    } else {
                        const data = await response.json();
                        document.getElementById("error").innerText = JSON.stringify(data, null, 2);
                    }
                }
            </script>
        </body>
    </html>
    """


# ============================
# RUN APP (LOCAL ONLY)
# ============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
