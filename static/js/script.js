const recordBtn = document.getElementById("recordBtn");
const resultText = document.getElementById("result");

let mediaRecorder;
let audioChunks = [];

recordBtn.addEventListener("click", async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordBtn.textContent = "🎤 Commencer l'enregistrement";
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
                    throw new Error("Le serveur a renvoyé une erreur.");
                }

                const data = await response.json();
                resultText.textContent = `Transcription : ${data.text}`;
            } catch (error) {
                console.error("Erreur:", error);
                resultText.textContent = "Erreur lors du traitement de l'audio. Vérifiez la console.";
            }
        };

        mediaRecorder.start();
        recordBtn.textContent = "🛑 Arrêter l'enregistrement";
    }
});
