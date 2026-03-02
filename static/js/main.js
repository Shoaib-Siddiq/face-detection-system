document.addEventListener('DOMContentLoaded', () => {
    const emotionEl = document.getElementById('currentEmotion');
    const container = document.body;
    let lastEmotion = "";

    async function updateEmotion() {
        try {
            const resp = await fetch('/emotion_status');
            const data = await resp.json();
            const emotion = data.emotion;

            if (emotion !== lastEmotion) {
                emotionEl.textContent = emotion;
                container.className = emotion.toLowerCase();
                console.log(`Emotion: ${emotion}`);
                lastEmotion = emotion;
            }
        } catch (e) {
            console.error("Failed to fetch emotion", e);
        }
    }

    setInterval(updateEmotion, 500); // Polling faster for "live" feel
});


