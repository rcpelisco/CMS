import os
import cv2
import pickle
import operator
import datetime
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cascades_dir = os.path.join(BASE_DIR, 'cascades', 'data', 'haarcascade_frontalface_default.xml')
image_dir = os.path.join(BASE_DIR, 'images')
profile_image_dir = os.path.join(BASE_DIR, '..', '..', 'static', 'img', 'profile_pictures')

face_cascade = cv2.CascadeClassifier(cascades_dir)

font_face = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self, name=None):
        self.video = cv2.VideoCapture(0)
        self.frames = 0
        self.labels = {}
        self.names = None
        self.data = []
        self.slug = ''
        self.name = name

        if not os.path.exists(os.path.join(BASE_DIR, 'pickle')):
            os.makedirs(os.path.join(BASE_DIR, 'pickle'))

        if not os.path.exists(os.path.join(BASE_DIR, 'training')):
            os.makedirs(os.path.join(BASE_DIR, 'training'))

        self.pickle_dir = os.path.join(BASE_DIR, 'pickle', 'labels.pickle')
        
        self.training_dir = os.path.join(BASE_DIR, 'training', 'data.yml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        try:
            with open(self.pickle_dir, 'rb') as f:
                self.labels = pickle.load(f)
                self.labels = {v:k for k, v in self.labels.items()}
            self.names = {v:0 for k, v in self.labels.items()}
            self.recognizer.read(self.training_dir)
        except IOError:
            print('file not found')

        if name is None:
            return 

        self.user_image_dir = os.path.join(image_dir, name)

        if not os.path.exists(self.user_image_dir):
            os.makedirs(self.user_image_dir)

        if not os.path.exists(profile_image_dir):
            os.makedirs(profile_image_dir)

        self.last_file = self.get_last_file(self.user_image_dir)

    def __del__(self):
        self.video.release()

    def detect(self, with_name=True, record=False, capture=False):
        ret, frame = self.video.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if capture:
            self.frames += 1
            now = datetime.datetime.now()
            w = 640
            h = 480
            y = 0
            x = (640 - 480) / 2
            cropped = frame[y: y + w,x: x + h]
            self.slug = self.name + '-' + now.strftime("%Y-%m-%d-%H-%M") + '.jpg'
            image_path = os.path.join(profile_image_dir, self.slug)
            cv2.imwrite(image_path, cropped)
            print(image_path)
            print(self.slug)

        for x, y, w, h in faces:
            if capture:
                continue
            roi_gray = gray[y: y + h, x: x + w]

            if with_name:
                id_, conf = self.recognizer.predict(roi_gray)

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

            if with_name:
                if conf >= 40:
                    self.frames += 1
                    self.names[self.labels[id_]] += 1
                    text = self.labels[id_] + ' - ' + str(conf)
                    color = (255, 255, 100)
                    stroke = 2
                    cv2.putText(frame, text, (x, y), font_face, 1, color, stroke, cv2.LINE_AA)

            if record: 
                self.frames += 1
                text = 'recording'
                color = (255, 255, 100)
                stroke = 2
                cv2.putText(frame, text, (x, y), font_face, 1, color, stroke, cv2.LINE_AA)
                cv2.imwrite(os.path.join(self.user_image_dir, 
                    str(self.frames + int(self.last_file)) + '.jpg'), roi_gray)
                print(os.path.join(self.user_image_dir, str(self.frames + int(self.last_file)) + '.jpg'))

        ret, jpeg = cv2.imencode('.jpg', frame)

        return {
            'image': jpeg.tobytes(),
            'frames': self.frames, 
            'patient': max(self.names.items(), key=operator.itemgetter(1))[0] if with_name else '',
            'image_path': self.slug
        }

    def get_last_file(self, user_image_dir):
        files_ = []
        last_file = 0
        for(root, dirs, files) in os.walk(user_image_dir):
            for file in files:
                files_.append(int(os.path.splitext(file)[0]))
                if len(files) == 0:
                    last_file = 0
                    break
                files_.sort()
                last_file = files_[-1]
        return last_file

class Trainer(object):
    def __init__(self):
        self.current_id = 0
        self.label_ids = {}
        self.pickle_dir = os.path.join(BASE_DIR, 'pickle', 'labels.pickle')
        self.training_dir = os.path.join(BASE_DIR, 'training', 'data.yml')
        self.y_labels = []
        self.x_train = []
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    def train(self):
        for(root, dirs, files) in os.walk(image_dir):
            for file in files:
                if file.endswith('png') or file.endswith('jpg'):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(' ', '-').lower()
                    if not label in self.label_ids:
                        self.label_ids[label] = self.current_id
                        self.current_id += 1
                    id_ = self.label_ids[label]
                    pil_image = Image.open(path).convert('L')
                    image_array = np.array(pil_image, 'uint8')

                    faces = face_cascade.detectMultiScale(image_array, scaleFactor = 1.01, minNeighbors = 5)
                    
                    for(x, y, w, h) in faces:
                        roi = image_array[y: y + h, x: x + w]
                        self.x_train.append(roi)
                        self.y_labels.append(id_)

        with open(self.pickle_dir, 'wb') as f:
            pickle.dump(self.label_ids, f)

        self.recognizer.train(self.x_train, np.array(self.y_labels))
        self.recognizer.save(self.training_dir)
        return 'success'
