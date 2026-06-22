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
        communicate = edge_tts.Communicate(
            chunk_text,
            VOICES[lang_key],
            rate="+0%",    # slower = more professional narration
            volume="+10%",
            pitch="-5Hz"    # slightly deeper = more authoritative
        )
        buf = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])
        buf.seek(0)
        return buf

    async def synthesize():
        from pydub import AudioSegment

        # Clean up text first
        import re
        cleaned = text.strip()

        # Split smartly — on punctuation + line breaks
        # Each sentence gets its own clip for precise pause control
        sentences = re.split(r'(?<=[।.!?])\s+', cleaned)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= 1:
            return await synthesize_chunk(cleaned)

        final_audio = AudioSegment.empty()

        for i, sentence in enumerate(sentences):
            chunk_buf = await synthesize_chunk(sentence)
            segment = AudioSegment.from_file(chunk_buf, format="mp3")

            # Decide pause length based on ending punctuation
            if sentence.endswith(('।', '.')):
                pause = AudioSegment.silent(duration=700)   # full stop — longer pause
            elif sentence.endswith(('!', '?')):
                pause = AudioSegment.silent(duration=800)   # dramatic pause
            elif sentence.endswith(','):
                pause = AudioSegment.silent(duration=300)   # comma — short pause
            elif sentence.endswith('...'):
                pause = AudioSegment.silent(duration=1000)  # ellipsis — suspense pause
            else:
                pause = AudioSegment.silent(duration=500)   # default

            final_audio += segment + pause

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