import requests
import os

url = "https://huggingface.co/Kaludi/emotion-detection-model/resolve/main/emotion-detection-model.onnx?download=true"
output = "emotion_model.onnx"

print(f"Downloading {url}...")
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(output, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Successfully downloaded to {output}")
    print(f"File size: {os.path.getsize(output) / 1024:.2f} KB")
else:
    print(f"Failed to download. Status code: {response.status_code}")
