from flask import Flask, render_template, request, jsonify
import os
import wave
import json
import vosk
import subprocess

app = Flask(__name__)

# Load the Vosk model
MODEL_PATH = "model/fr"
if not os.path.exists(MODEL_PATH):
    raise ValueError("Vosk model not found!")

model = vosk.Model(MODEL_PATH)

@app.route("/")
def index():
    return render_template("index.html")  # Serve the HTML page

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    webm_path = "temp.webm"
    wav_path = "temp.wav"
    audio_file.save(webm_path)

    # Convert WebM to WAV using FFmpeg
    conversion_cmd = [
        "ffmpeg", "-i", webm_path,
        "-ar", "16000",  # Sample rate 16kHz (required by Vosk)
        "-ac", "1",  # Mono channel (required by Vosk)
        "-c:a", "pcm_s16le",  # 16-bit PCM format
        wav_path
    ]

    subprocess.run(conversion_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Open the converted WAV file
    with wave.open(wav_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            return jsonify({"error": "Audio file must be WAV format, mono PCM"}), 400

        rec = vosk.KaldiRecognizer(model, wf.getframerate())

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            rec.AcceptWaveform(data)

        result = json.loads(rec.Result())

    # Clean up temporary files
    os.remove(webm_path)
    os.remove(wav_path)

    return jsonify({"text": result.get("text", "")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
