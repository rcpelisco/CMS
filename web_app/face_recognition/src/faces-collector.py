import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cascades_dir = os.path.join(BASE_DIR, '..', 'cascades', 'data', 'haarcascade_frontalface_default.xml')
image_dir = os.path.join(BASE_DIR, '..', 'images')

font_face = cv2.FONT_HERSHEY_SIMPLEX

face_cascade = cv2.CascadeClassifier(cascades_dir)
cap = cv2.VideoCapture(0)

recording = False
frames = 0

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

name = raw_input('Name: ')
user_image_dir = os.path.join(image_dir, name).replace(' ', '-').lower()
if not os.path.exists(user_image_dir):
    os.makedirs(user_image_dir)

last_file = get_last_file(user_image_dir)

