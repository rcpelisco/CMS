from flask import Blueprint, render_template, redirect, request, Response
from face_recognition import detector
import os
import cv2
import pickle
import numpy as np

module = Blueprint('face_recognition', __name__, template_folder='templates')

@module.route('/')
def index():
    print(pickle_dir)
    return render_template('face_recognition/index.html')

@module.route('/detect_face')
def detect_face():
    detector()
    return redirect(redirect_url())

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)