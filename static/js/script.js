const recordBtn = document.getElementById("recordBtn");
const resultText = document.getElementById("result");

let mediaRecorder;
let audioChunks = [];

recordBtn.addEventListener("click", async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordBtn.textContent = "🎤 Start Recording";
    } else {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });

        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            const formData = new FormData();
            formData.append("audio", audioBlob, "audio.webm");

            try {
                const response = await fetch("/transcribe", {
                    method: "POST",
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error("Server returned an error.");
                }

                const data = await response.json();
                resultText.textContent = `Transcription: ${data.text}`;
            } catch (error) {
                console.error("Error:", error);
                resultText.textContent = "Error processing audio. Check console.";
            }
        };

        mediaRecorder.start();
        recordBtn.textContent = "🛑 Stop Recording";
    }
});
