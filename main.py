import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# ---------------------------------------------------------
# MASTER HEGAY AI STYLE PROMPT
# ---------------------------------------------------------
HEGAY_AI_MASTER_PROMPT = """
Hegay AI Master Style Guide:

Create visuals in a unified Afro‑cinematic, diaspora‑focused, modern digital art style.
All outputs must be clean, professional, emotionally powerful, and culturally respectful.

CORE VISUAL STYLE:
- Afro‑cinematic lighting with soft glow and deep contrast
- Smooth gradients, clean edges, sharp details
- Melanin‑rich skin tones, expressive eyes, natural textures
- Vibrant but balanced colors inspired by African culture
- Subtle bloom, depth, and atmospheric richness
- Professional studio‑grade finish

CULTURAL IDENTITY:
- Nigerian + African diaspora representation
- Ankara, Aso‑oke, tribal patterns, Afro‑fusion fashion
- Yoruba, Igbo, Hausa, Pidgin, and diaspora influences
- Empowering, respectful, uplifting portrayal of African people

FORMAT ADAPTATION:
- Music Covers: bold composition, emotional storytelling, album‑ready layout
- Drama Posters: cinematic framing, film‑grade lighting, title space preserved
- Avatars: centered portrait, clean background, afro‑futuristic polish
- Logos: minimalist vector‑style shapes, flat design, no background
- Social Cards: mobile‑first layout, bold headline space, high contrast
- YouTube Thumbnails: expressive subject, strong contrast, 16:9, text space
- Future Video Frames: consistent style, smooth motion, cinematic tone

TECHNICAL QUALITY:
- Ultra‑sharp details
- High dynamic range
- Clean color grading
- No artifacts or distortions
- No copyrighted characters, logos, or branded elements

OUTPUT REQUIREMENT:
Always produce a polished, emotionally powerful, diaspora‑focused visual
in the unified Hegay AI signature style.
"""

# ---------------------------------------------------------
# HELPER FUNCTION — Stability SD3
# ---------------------------------------------------------
def generate_stability_image(full_prompt: str):
    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json"
    }

    files = {
        "prompt": (None, full_prompt),
        "output_format": (None, "png")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return None, response.text

    result = response.json()
    return result.get("image"), None

# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Hegay AI backend is running successfully on Render."})

# ---------------------------------------------------------
# GENERIC IMAGE ENDPOINT
# ---------------------------------------------------------
@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    full_prompt = f"{prompt}. {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_stability_image(full_prompt)

    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500

    return jsonify({"image": image_base64})

# ---------------------------------------------------------
# MUSIC COVER
# ---------------------------------------------------------
@app.route("/generate-music-cover", methods=["POST"])
def generate_music_cover():
    data = request.get_json()
    prompt = data.get("prompt", "")

    style = "Album cover style, bold composition, emotional storytelling."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_stability_image(full_prompt)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64})

# ---------------------------------------------------------
# DRAMA POSTER
# ---------------------------------------------------------
@app.route("/generate-drama-poster", methods=["POST"])
def generate_drama_poster():
    data = request.get_json()
    prompt = data.get("prompt", "")

    style = "Drama poster style, cinematic framing, title space preserved."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_stability_image(full_prompt)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64})

# ---------------------------------------------------------
# AVATAR
# ---------------------------------------------------------
@app.route("/generate-avatar", methods=["POST"])
def generate_avatar():
    data = request.get_json()
    prompt = data.get("prompt", "")

    style = "Portrait avatar style, centered, clean background."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_stability_image(full_prompt)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64})

# ---------------------------------------------------------
# LOGO
# ---------------------------------------------------------
@app.route("/generate-logo", methods=["POST"])
def generate_logo():
    data = request.get_json()
    prompt = data.get("prompt", "")

    style = "Minimalist vector logo, flat design, no background."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_stability_image(full_prompt)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64})

# ---------------------------------------------------------
# SOCIAL CARD
# ---------------------------------------------------------
@app.route("/generate-social-card", methods=["POST"])
def generate_social_card():
    data = request.get_json()
    prompt = data.get("prompt", "")

    style = "Social media promo card, mobile-first layout, bold headline space."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_stability_image(full_prompt)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64})

# ---------------------------------------------------------
# YOUTUBE THUMBNAIL
# ---------------------------------------------------------
@app.route("/generate-youtube-thumbnail", methods=["POST"])
def generate_youtube_thumbnail():
    data = request.get_json()
    prompt = data.get("prompt", "")

    style = "YouTube thumbnail style, expressive subject, strong contrast, 16:9."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_stability_image(full_prompt)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64})

# ---------------------------------------------------------
# IMAGE TEST PAGE
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
