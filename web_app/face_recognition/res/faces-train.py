import os
import cv2
import pickle
import numpy as np
from PIL import Image
    
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, '..', 'images')
cascades_dir = os.path.join(BASE_DIR, '..', 'cascades', 'data')
pickle_dir = os.path.join(BASE_DIR, '..',  'pickle', 'labels.pickle')
training_dir = os.path.join(BASE_DIR, '..', 'training', 'data.yml')
    
face_cascade = cv2.CascadeClassifier(os.path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml'))
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

print('Collecting data ...')
for(root, dirs, files) in os.walk(image_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg'):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(' ', '-').lower()
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            pil_image = Image.open(path).convert('L')
            image_array = np.array(pil_image, 'uint8')

            faces = face_cascade.detectMultiScale(image_array, scaleFactor = 1.01, minNeighbors = 5)
            
            for(x, y, w, h) in faces:
                roi = image_array[y: y + h, x: x + w]
                x_train.append(roi)
                y_labels.append(id_)

with open(pickle_dir, 'wb') as f:
    pickle.dump(label_ids, f)

print('Training ...')
recognizer.train(x_train, np.array(y_labels))
print('Saving ...')
recognizer.save(training_dir)
