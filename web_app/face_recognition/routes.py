from flask import Blueprint, render_template
from flask import redirect, request, Response, url_for
from res.camera import VideoCamera
from ..site.extra import get

module = Blueprint('face_recognition', __name__, template_folder='templates')

@module.route('/')
def index():
    return render_template('face_recognition/index.html')

@module.route('/a')
def a():
    print('a was called')
    return redirect(url_for('patients.show', patient=1))

def gen(camera, valid):
    while valid:
        data = camera.get()
        image = data['image']
        frames = data['frames']
        patient = data['patient']
        print(frames)
        if(frames == 20):
            get('/face_recognition/a')
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')

@module.route('/video_feed')
def video_feed():
    print('video_feed')
    return Response(gen(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')