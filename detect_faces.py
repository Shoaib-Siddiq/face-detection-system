import cv2
import os
import numpy as np

class FaceDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.last_emotion = "Initializing"
        
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"Haar Cascade not found at {cascade_path}")
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Initialize Emotion Detection Model (FERPlus 64x64 Grayscale)
        model_path = 'emotion_model.onnx'
        if os.path.exists(model_path):
            try:
                self.emotion_net = cv2.dnn.readNetFromONNX(model_path)
                self.emotions = ['Neutral', 'Happy', 'Surprise', 'Sad', 'Anger', 'Disgust', 'Fear', 'Contempt']
            except Exception as e:
                self.emotion_net = None
                print(f"Error loading emotion model: {e}")
        else:
            self.emotion_net = None
            print("Warning: emotion_model.onnx not found. Emotion detection disabled.")

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        current_emotion = "Neutral"

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 191, 0), 2)
            
            if self.emotion_net:
                try:
                    # Preprocessing for FERPlus (64x64 Grayscale)
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (64, 64))
                    blob = cv2.dnn.blobFromImage(face_roi, 1.0, (64, 64), (0), swapRB=False, crop=False)
                    
                    self.emotion_net.setInput(blob)
                    preds = self.emotion_net.forward()
                    emotion_idx = np.argmax(preds[0])
                    
                    if emotion_idx < len(self.emotions):
                        current_emotion = self.emotions[emotion_idx]
                    
                    cv2.putText(frame, current_emotion, (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 191, 0), 2)
                except Exception as e:
                    print(f"Inference error: {e}")

        self.last_emotion = current_emotion

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return None
        return jpeg.tobytes()

    def __del__(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()




