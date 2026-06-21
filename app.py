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

    async def synthesize_chunk(chunk_text):
    communicate = edge_tts.Communicate(chunk_text, VOICES[lang_key], rate="+5%", volume="+10%")
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    buf.seek(0)
    return buf

    async def synthesize():
        from pydub import AudioSegment

        # Split text into paragraphs (on double line breaks or single line breaks)
        paragraphs = [p.strip() for p in text.replace("\r\n", "\n").split("\n") if p.strip()]

        if len(paragraphs) <= 1:
            # No paragraph breaks — just synthesize normally
            return await synthesize_chunk(text)

        silence = AudioSegment.silent(duration=600)  # 600ms pause between paragraphs
        final_audio = AudioSegment.empty()

        for para in paragraphs:
            chunk_buf = await synthesize_chunk(para)
            segment = AudioSegment.from_file(chunk_buf, format="mp3")
            final_audio += segment + silence

        out_buf = io.BytesIO()
        final_audio.export(out_buf, format="mp3")
        out_buf.seek(0)
        return out_buf

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