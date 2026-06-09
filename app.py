from flask import Flask, request, jsonify, send_file, render_template
import os
import edge_tts
import asyncio
import io

app = Flask(__name__)

# Neural voices - Indian English & Hindi
VOICES = {
    "english_indian": "en-IN-NeerjaNeural",   # warm female narrator
    "english_indian_male": "en-IN-PrabhatNeural", # calm male narrator
    "hindi": "hi-IN-SwaraNeural",             # expressive female Hindi
    "hindi_male": "hi-IN-MadhurNeural",       # deep male Hindi
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text     = (data.get("text") or "").strip()
    lang_key = data.get("language", "english_indian")

    if not text:
        return jsonify({"error": "No text provided"}), 400
    if lang_key not in VOICES:
        return jsonify({"error": "Unsupported language"}), 400

    voice = VOICES[lang_key]

    async def synthesize():
        communicate = edge_tts.Communicate(text, voice, rate="-5%", volume="+10%")
        buf = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])
        buf.seek(0)
        return buf

    try:
        buf = asyncio.run(synthesize())
        return send_file(buf, mimetype="audio/mpeg",
                         download_name="vaani_narration.mp3", as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n🎙️  Vaani TTS is running!")
    print("👉  Open your browser at: http://localhost:5000\n")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))