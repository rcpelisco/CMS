from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from ..models.models import Patient
from ..models.models import User
from ..models.models import FaceRecognition
from ..models.schema import PatientSchema
from ..models.schema import UserSchema
from ..models.schema import FaceRecognitionSchema

module = Blueprint('api.face_recognition', __name__)

face_recognition_schema = FaceRecognitionSchema()
patient_schema = PatientSchema()
user_schema = UserSchema()

@module.route('/', methods=['GET'])
def index():
    face_recognition = FaceRecognition.query.get(1)
    if face_recognition is None:
        return jsonify({'message': 'Face recognition record not found!'}), 400
    face_recognition, errors = face_recognition_schema.dump(face_recognition)
    patient = Patient.query.filter(Patient.slug == face_recognition['name']).one()
    patient, errors = patient_schema.dump(patient)
    return jsonify({'patient': patient})

@module.route('/login', methods=['GET'])
def login():
    face_recognition = FaceRecognition.query.get(1)
    if face_recognition is None:
        return jsonify({'message': 'Face recognition record not found!'}), 400
    face_recognition, errors = face_recognition_schema.dump(face_recognition)
    user = User.query.filter(User.slug == face_recognition['name']).one()
    user, errors = user_schema.dump(user)
    return jsonify({'user': user})

@module.route('/', methods=['POST'])
def store():
    json_data = request.get_json()

    face_recognition = None
    
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    
    message = 'Medical record updated'
    face_recognition = FaceRecognition.query.get(1)

    if face_recognition is None:
        message = 'Medical record created'
        face_recognition = FaceRecognition()

    face_recognition.name = json_data['name']
    face_recognition.save()

    face_recognition, errors = face_recognition_schema.dump(face_recognition)

    return jsonify({'message': message, 'face_recognition': face_recognition})
