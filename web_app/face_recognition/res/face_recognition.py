import os
import cv2
import pickle
import numpy as np
from PIL import Image

def show_window():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

show_window()