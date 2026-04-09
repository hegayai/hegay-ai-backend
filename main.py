from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

@app.get("/")
def home():
    return "Hegay AI Backend is running on Render."


# ---------------- TEXT GENERATION ----------------

@app.post("/generate-text")
def generate_text():
    data = request.json or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    return jsonify({
        "prompt": prompt,
        "response": f"You said: {prompt}"
    })


# ---------------- IMAGE GENERATION (PUBLIC SD 1.5) ----------------

@app.post("/generate-image")
def generate_image():
    data = request.json or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        # Public SD 1.5 endpoint (no auth)
        response = requests.post(
            "https://hf.space/embed/fffiloni/stable-diffusion-1-5/api/predict/",
            json={"data": [prompt]}
        )

        result = response.json()

        # Extract base64 image
        image_base64 = result["data"][0].split(",")[1]

        return jsonify({"image_url": f"data:image/png;base64,{image_base64}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- IMAGE TEST PAGE ----------------

@app.get("/image-test")
def image_test_page():
    return """
    <html>
    <body>
    <h2>Test Image Generator (Stable Diffusion 1.5 — Render)</h2>

    <textarea id="prompt" rows="4" cols="60">Beautiful African woman in sunlight</textarea><br><br>

    <button onclick="send()">Generate</button>

    <p id="status"></p>
    <img id="img" style="max-width:512px; display:none;" />

    <script>
    function send() {
      const prompt = document.getElementById("prompt").value;
      const status = document.getElementById("status");
      const img = document.getElementById("img");

      status.textContent = "Generating...";
      img.style.display = "none";

      fetch("/generate-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      })
        .then(r => r.json())
        .then(d => {
          if (d.error) {
            status.textContent = "Error: " + d.error;
            return;
          }

          status.textContent = "Done";
          img.src = d.image_url;
          img.style.display = "block";
        });
    }
    </script>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
