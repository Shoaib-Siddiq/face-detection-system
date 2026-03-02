from flask import Flask, render_template, Response
from detect_faces import FaceDetector

app = Flask(__name__)
detector = FaceDetector()

@app.route('/')
def index():
    return render_template('index.html')

def gen(detector):
    while True:
        frame = detector.get_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(detector),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/emotion_status')
def emotion_status():
    return {"emotion": detector.last_emotion}

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True)
