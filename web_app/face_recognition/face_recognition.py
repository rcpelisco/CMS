import os
import cv2
import pickle
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cascades_dir = os.path.join(BASE_DIR, 'cascades', 'data', 'haarcascade_frontalface_default.xml')
image_dir = os.path.join(BASE_DIR, 'images')
pickle_dir = os.path.join(BASE_DIR,  'pickle', 'labels.pickle')
training_dir = os.path.join(BASE_DIR, 'training', 'data.yml')

font_face = cv2.FONT_HERSHEY_SIMPLEX

labels = {}
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(training_dir)

face_cascade = cv2.CascadeClassifier(cascades_dir)
cap = cv2.VideoCapture(0)

recording = False
frames = 0

with open(pickle_dir, 'rb') as f:
    labels = pickle.load(f)
    labels = {v:k for k, v in labels.items()}

def get_last_file(user_image_dir):
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
name = ''
user_image_dir = os.path.join(image_dir, name).replace(' ', '-').lower()
if not os.path.exists(user_image_dir):
    os.makedirs(user_image_dir)

last_file = get_last_file(user_image_dir)

def collector():
    while(True):
        key = cv2.waitKey(20)

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5)

        for(x, y, w, h) in faces:
            roi_gray = gray[y: y + h, x: x + w]

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

            if frames >= 5:
                recording = False
                frames = 0

            if recording:
                frames += 1

                text = 'recording frame ' + str(frames) + '/5'
                color = (0, 250, 255)
                stroke = 1
                cv2.putText(frame, text, (x, y), font_face, .50, color, stroke, cv2.LINE_AA)

                cv2.imwrite(os.path.join(user_image_dir, str(frames + int(last_file)) + '.jpg'), roi_gray)
                print(os.path.join(user_image_dir, str(frames + int(last_file)) + '.jpg'))
                continue

            text = 'Press `r` to record'
            color = (84, 255, 81)
            stroke = 1
            cv2.putText(frame, text, (x, y), font_face, .75, color, stroke, cv2.LINE_AA)

        cv2.imshow('frame', frame)

        if(key & 0xFF == ord('r')):
            last_file = get_last_file(user_image_dir)
            recording = True

        if(key & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()

def detector():
    while(True):
        key = cv2.waitKey(20)
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5)

        for(x, y, w, h) in faces:
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
                text = labels[id_] + ' - ' + str(conf)
                color = (255, 255, 100)
                stroke = 2
                cv2.putText(frame, text, (x, y), font_face, 1, color, stroke, cv2.LINE_AA)
            
            print(conf)

        cv2.imshow('frame', frame)
        if(key & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()