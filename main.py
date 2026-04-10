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

# Example model IDs (you must set the real ones in Render):
# e.g. "black-forest-labs/flux-1-dev"
# e.g. "playgroundai/playground-v3.0"
FLUX_MODEL_ID = os.getenv("FLUX_MODEL_ID")          # primary realism model
PLAYGROUND_MODEL_ID = os.getenv("PLAYGROUND_MODEL_ID")  # cinematic / group model

DEEPINFRA_BASE_URL = "https://api.deepinfra.com/v1/inference"

# ---------------------------------------------------------
# MASTER HEGAY AI STYLE PROMPT
# ---------------------------------------------------------
HEGAY_AI_MASTER_PROMPT = """
Hegay AI Master Style Guide:

Create visuals in a unified Afro‑cinematic, diaspora‑focused, modern digital art style
with a touch of high-end animated film quality (Pixar-level polish but original, non-copyrighted).

FACES, BODIES & CONSISTENT CHARACTERS:
- Natural, beautiful faces with correct anatomy and proportions
- Clear eyes, correct hands and fingers, no extra limbs or distortions
- Consistent character look when the same description is reused
  (same face, age, hairstyle, vibe, and general appearance across scenes)
- Expressive but believable emotions
- Respectful, dignified, uplifting portrayal of all people

DIVERSE PEOPLE & CULTURES:
- Support African, African diaspora, American, European, Asian, Indian, Middle Eastern,
  Latin American and other global identities
- Cultural attire, environments, and settings should match the description
  (e.g. saree, kimono, agbada, suit, streetwear, etc.)
- Always avoid stereotypes; focus on beauty, strength, and humanity

CORE VISUAL STYLE:
- Afro‑cinematic lighting with soft glow and deep contrast
- Smooth gradients, clean edges, sharp details
- Rich skin tones, detailed fabrics, realistic or stylized hair
- Vibrant but balanced colors inspired by global cultures
- Subtle bloom, depth, and atmospheric richness
- Professional studio‑grade finish

FORMAT ADAPTATION:
- Music Covers: bold composition, album‑ready layout, emotional storytelling
- Drama Posters: cinematic framing, film‑grade lighting, title space preserved
- Avatars: centered portrait, clean background, afro‑futuristic or modern polish
- Logos: minimalist vector‑style shapes, flat design, no background
- Social Cards: mobile-first layout, bold headline space, high contrast
- YouTube Thumbnails: expressive subject, strong contrast, 16:9, text space
- Future Video Frames: consistent style, smooth motion, cinematic tone

QUALITY TARGET:
- Match or exceed the visual clarity, sharpness, and cleanliness
  of leading AI image models
- Ultra‑sharp details, high dynamic range, clean color grading
- No artifacts, no glitches, no text unless requested
- No copyrighted characters, logos, or branded elements

OUTPUT REQUIREMENT:
Always produce a polished, emotionally powerful, globally inclusive visual
in the unified Hegay AI signature style.
"""

# ---------------------------------------------------------
# MODEL SWITCHER HELPER
# ---------------------------------------------------------
def get_model_id(model_name: str) -> str:
    """
    Returns the correct model ID based on the requested model.
    Defaults to FLUX_MODEL_ID if unknown.
    """
    if model_name == "playground":
        return PLAYGROUND_MODEL_ID
    # default to flux
    return FLUX_MODEL_ID

def generate_image_with_model(full_prompt: str, model_name: str = "flux"):
    """
    Calls DeepInfra (or similar provider) with the selected model.
    You must set:
      - DEEPINFRA_API_KEY
      - FLUX_MODEL_ID
      - PLAYGROUND_MODEL_ID
    in your environment.
    """
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
        # You can add more provider-specific params here if needed:
        # "num_inference_steps": 28,
        # "guidance_scale": 4.5,
        # "width": 1024,
        # "height": 1024,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return None, response.text

    try:
        result = response.json()
    except Exception as e:
        return None, f"Failed to parse JSON: {str(e)}"

    # Try common patterns: some providers return "images" with base64,
    # others may return "image" directly. We support both.
    image_base64 = None

    if isinstance(result, dict):
        if "images" in result and isinstance(result["images"], list) and result["images"]:
            # e.g. {"images": [{"image_base64": "..."}]}
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
    model = data.get("model", "flux")  # "flux" or "playground"

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
# IMAGE TEST PAGE (uses /generate-image with default model)
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
