import os
import cv2
import pickle
import operator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cascades_dir = os.path.join(BASE_DIR, 'cascades', 'data', 'haarcascade_frontalface_default.xml')
pickle_dir = os.path.join(BASE_DIR, 'pickle', 'labels.pickle')
training_dir = os.path.join(BASE_DIR, 'training', 'data.yml')

face_cascade = cv2.CascadeClassifier(cascades_dir)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(training_dir)

font_face = cv2.FONT_HERSHEY_SIMPLEX

labels = {}

with open(pickle_dir, 'rb') as f:
    labels = pickle.load(f)
    labels = {v:k for k, v in labels.items()}

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.frames = 0
        self.names = {v:0 for k, v in labels.items()}
        self.data = []

    def __del__(self):
        self.video.release()

    def get(self):
        ret, frame = self.video.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:
            roi_gray = gray[y: y + h, x: x + w]
            id_, conf = recognizer.predict(roi_gray)

            color = (255, 0, 0)
            stroke = 2
            end_coord_x = x + w
            end_coord_y = y + h
            cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y), color, stroke)

            if w <= 150 and h <= 150:
                text = 'face is too far!'
                color = (10, 10, 200)
                stroke = 2
                cv2.putText(frame, text, (x, y), font_face, .75, color, stroke, cv2.LINE_AA)
                continue

            if conf >= 40:
                self.frames += 1
                self.names[labels[id_]] += 1
                text = labels[id_] + ' - ' + str(conf)
                color = (255, 255, 100)
                stroke = 2
                cv2.putText(frame, text, (x, y), font_face, 1, color, stroke, cv2.LINE_AA)
                
        ret, jpeg = cv2.imencode('.jpg', frame)
        return {'image': jpeg.tobytes(), 
            'frames': self.frames, 
            'patient': max(self.names.items(), key=operator.itemgetter(1))[0]
        }

