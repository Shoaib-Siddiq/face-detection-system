document.addEventListener('DOMContentLoaded', () => {
    const videoFeed = document.getElementById('videoFeed');
    const toggleBtn = document.getElementById('toggleFeed');
    const logContent = document.getElementById('logContent');
    let isLive = true;

    function addLog(message) {
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        const now = new Date();
        const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
        entry.textContent = `[${time}] ${message}`;
        logContent.prepend(entry);
    }

    toggleBtn.addEventListener('click', () => {
        isLive = !isLive;
        if (isLive) {
            videoFeed.src = "/video_feed";
            toggleBtn.textContent = 'Pause Feed';
            toggleBtn.classList.remove('active');
            addLog("System feed resumed.");
        } else {
            videoFeed.src = "";
            toggleBtn.textContent = 'Resume Feed';
            toggleBtn.classList.add('active');
            addLog("System feed paused.");
        }
    });

    // Initial logs
    addLog("System handshake verified.");
    addLog("Neural network loaded.");
    addLog("Face detection engine started.");
    addLog("Emotion analysis core initialized.");

    // Real-time Emotion Polling
    const emotionEl = document.getElementById('currentEmotion');
    const sentimentCard = document.querySelector('.sentiment-card');
    let lastEmotion = "";

    async function updateEmotion() {
        if (!isLive) return;
        try {
            const resp = await fetch('/emotion_status');
            const data = await resp.json();
            const emotion = data.emotion;

            if (emotion !== lastEmotion) {
                emotionEl.textContent = emotion;
                sentimentCard.className = `card sentiment-card ${emotion.toLowerCase()}`;
                addLog(`Detected Emotion: ${emotion}`);
                lastEmotion = emotion;
            }
        } catch (e) {
            console.error("Failed to fetch emotion", e);
        }
    }

    setInterval(updateEmotion, 1000);
});

