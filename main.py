import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------
# ENVIRONMENT VARIABLES (SET THESE IN RENDER)
# ---------------------------------------------------------
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

# Example model IDs (set these in Render)
# Flux.1 (realism, faces, consistency)
FLUX_MODEL_ID = os.getenv("FLUX_MODEL_ID")  # black-forest-labs/flux-1-dev

# Playground v3 (cinematic, group scenes)
PLAYGROUND_MODEL_ID = os.getenv("PLAYGROUND_MODEL_ID")  # playgroundai/playground-v3.0

DEEPINFRA_BASE_URL = "https://api.deepinfra.com/v1/inference"

# ---------------------------------------------------------
# MASTER HEGAY AI STYLE PROMPT (UPGRADED)
# ---------------------------------------------------------
HEGAY_AI_MASTER_PROMPT = """
Hegay AI Master Style Guide:

Create visuals in a unified Afro‑cinematic, diaspora‑focused, modern digital art style
with a touch of high-end animated film quality (Pixar-level polish but original).

FACE & CHARACTER QUALITY:
- Natural, beautiful faces with correct anatomy
- Clear eyes, correct hands, no distortions
- Accurate age representation (e.g., “32-year-old woman” must look 32)
- Consistent characters across multiple images when the same description is used
- Expressive but believable emotions

GLOBAL DIVERSITY:
- Support African, diaspora, American, European, Asian, Indian, Middle Eastern,
  Latin American and global identities
- Cultural attire and environments must match the description
- Avoid stereotypes; focus on dignity, beauty, and humanity

CINEMATIC STYLE:
- Deep contrast, soft glow, dramatic lighting
- Rich melanin tones, detailed fabrics, realistic or stylized hair
- Smooth gradients, clean edges, sharp details
- Vibrant but balanced colors inspired by global cultures
- Subtle bloom, depth, atmospheric richness

FORMAT ADAPTATION:
- Music Covers: bold composition, album-ready layout
- Drama Posters: cinematic framing, film-grade lighting
- Avatars: centered portrait, clean background
- Logos: minimalist vector shapes, no background
- Social Cards: mobile-first layout, bold headline space
- YouTube Thumbnails: expressive subject, strong contrast, 16:9
- Future Video Frames: consistent style, smooth motion

QUALITY TARGET:
- Match or exceed top AI models in clarity and realism
- Ultra-sharp details, high dynamic range, clean color grading
- No artifacts, no glitches, no unwanted text
- No copyrighted characters or branded elements

OUTPUT REQUIREMENT:
Always produce a polished, emotionally powerful, globally inclusive visual
in the unified Hegay AI signature style.
"""

# ---------------------------------------------------------
# MODEL SWITCHER
# ---------------------------------------------------------
def get_model_id(model_name: str) -> str:
    if model_name == "playground":
        return PLAYGROUND_MODEL_ID
    return FLUX_MODEL_ID  # default

def generate_image_with_model(full_prompt: str, model_name: str = "flux"):
    if not DEEPINFRA_API_KEY:
        return None, "DEEPINFRA_API_KEY is not set"

    model_id = get_model_id(model_name)
    if not model_id:
        return None, f"Model ID for '{model_name}' is not configured"

    url = f"{DEEPINFRA_BASE_URL}/{model_id}"

    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": full_prompt
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return None, response.text

    try:
        result = response.json()
    except Exception as e:
        return None, f"Failed to parse JSON: {str(e)}"

    image_base64 = None

    if isinstance(result, dict):
        if "images" in result and isinstance(result["images"], list) and result["images"]:
            first = result["images"][0]
            image_base64 = first.get("image_base64") or first.get("image")
        elif "image" in result:
            image_base64 = result.get("image")

    if not image_base64:
        return None, f"Could not find image data in response: {result}"

    return image_base64, None

# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Hegay AI backend (Flux + Playground switcher) is running successfully."})

# ---------------------------------------------------------
# TEXT GENERATION (placeholder)
# ---------------------------------------------------------
@app.route("/generate-text", methods=["POST"])
def generate_text():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    return jsonify({
        "response": f"You said: {prompt}. Text generation model will be added soon."
    })

# ---------------------------------------------------------
# GENERIC IMAGE ENDPOINT
# ---------------------------------------------------------
@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt")
    model = data.get("model", "flux")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    full_prompt = f"{prompt}. {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_image_with_model(full_prompt, model_name=model)

    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500

    return jsonify({"image": image_base64, "model_used": model})

# ---------------------------------------------------------
# MUSIC COVER
# ---------------------------------------------------------
@app.route("/generate-music-cover", methods=["POST"])
def generate_music_cover():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = data.get("model", "flux")

    style = "Album cover style, bold composition, emotional storytelling."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_image_with_model(full_prompt, model_name=model)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64, "model_used": model})

# ---------------------------------------------------------
# DRAMA POSTER
# ---------------------------------------------------------
@app.route("/generate-drama-poster", methods=["POST"])
def generate_drama_poster():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = data.get("model", "flux")

    style = "Drama poster style, cinematic framing, title space preserved."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_image_with_model(full_prompt, model_name=model)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64, "model_used": model})

# ---------------------------------------------------------
# AVATAR
# ---------------------------------------------------------
@app.route("/generate-avatar", methods=["POST"])
def generate_avatar():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = data.get("model", "flux")

    style = "Portrait avatar style, centered, clean background."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_image_with_model(full_prompt, model_name=model)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64, "model_used": model})

# ---------------------------------------------------------
# LOGO
# ---------------------------------------------------------
@app.route("/generate-logo", methods=["POST"])
def generate_logo():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = data.get("model", "flux")

    style = "Minimalist vector logo, flat design, no background."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_image_with_model(full_prompt, model_name=model)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64, "model_used": model})

# ---------------------------------------------------------
# SOCIAL CARD
# ---------------------------------------------------------
@app.route("/generate-social-card", methods=["POST"])
def generate_social_card():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = data.get("model", "flux")

    style = "Social media promo card, mobile-first layout, bold headline space."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_image_with_model(full_prompt, model_name=model)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64, "model_used": model})

# ---------------------------------------------------------
# YOUTUBE THUMBNAIL
# ---------------------------------------------------------
@app.route("/generate-youtube-thumbnail", methods=["POST"])
def generate_youtube_thumbnail():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = data.get("model", "flux")

    style = "YouTube thumbnail style, expressive subject, strong contrast, 16:9."
    full_prompt = f"{prompt}. {style} {HEGAY_AI_MASTER_PROMPT}"

    image_base64, error = generate_image_with_model(full_prompt, model_name=model)
    if error or not image_base64:
        return jsonify({"error": "Image generation failed", "details": error}), 500
    return jsonify({"image": image_base64, "model_used": model})

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
        <h2>Hegay AI – Image Generator Test (Flux / Playground)</h2>
        <p>Default model: <b>flux</b>. You can change it in code or build a UI toggle later.</p>
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
                    document.getElementById("status").innerText = "Done. Model used: " + data.model_used;
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
