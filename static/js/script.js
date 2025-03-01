const recordBtn = document.getElementById("recordBtn");
const resultText = document.getElementById("result");

let mediaRecorder;
let audioChunks = [];

recordBtn.addEventListener("click", async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordBtn.textContent = "🎤 Commencer l'enregistrement";
    } else {
        try {
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

                // Disable the button and show loading state
                recordBtn.disabled = true;
                recordBtn.textContent = "🔄 Chargement..."; // Indicate loading

                try {
                    const response = await fetch("/transcribe", {
                        method: "POST",
                        body: formData,
                    });

                    // Check if the response is OK, otherwise throw an error
                    if (!response.ok) {
                        const errorData = await response.json();  // Get error details from the backend
                        throw new Error(errorData.error || "Le serveur a renvoyé une erreur.");
                    }

                    const data = await response.text();
                    
                    resultText.textContent = `Transcription : ${data}`;
                } catch (error) {
                    console.error("Erreur:", error);
                    resultText.textContent = `Erreur: ${error.message || "Erreur inconnue"}`;
                } finally {
                    // Re-enable the button and reset its text after the operation
                    recordBtn.disabled = false;
                    recordBtn.textContent = "🎤 Commencer l'enregistrement";  // Reset button text
                }
            };

            mediaRecorder.start();
            recordBtn.textContent = "🛑 Arrêter l'enregistrement";
        } catch (error) {
            // Handle errors related to starting the recording process
            console.error("Erreur d'accès au microphone:", error);
            resultText.textContent = "Impossible d'accéder au microphone. Assurez-vous qu'il est bien connecté.";
        }
    }
});
