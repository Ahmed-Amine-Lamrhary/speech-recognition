import subprocess
import json
import wave
import vosk
import os

MODEL_PATH = "model/fr"
if not os.path.exists(MODEL_PATH):
    raise ValueError("Vosk model not found!")

model = vosk.Model(MODEL_PATH)

def get_text_from_audio(audio_file):
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
            return {"error": "Audio file must be WAV format, mono PCM"}

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
    
    text = result.get("text", "")

    # Check if text is empty, raise an exception in French if it is
    if not text.strip():
        raise Exception("Le texte n'était pas reconnu. Veuillez essayer un autre enregistrement audio.")

    return text
