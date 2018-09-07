from flask import Blueprint, jsonify, request
from ..models.patient import Patient

module = Blueprint('api.patients', __name__)

@module.route('/', methods=['GET'])
def index():
    patients = Patient().all()
    return jsonify({'data': patients})

@module.route('/<patient>', methods=['GET'])
def show(patient):
    patient = Patient().find(patient)
    return jsonify(patient)
    
@module.route('/', methods=['PUT', 'POST'])
def store():
    data = request.get_json()
    patient = Patient()

    if request.method == 'PUT' and 'id' in data:
        patient.find(data['id'])
    
    patient.first_name = data['first_name']
    patient.last_name = data['last_name']
    patient.gender = data['gender']
    patient.civil_status = data['civil_status']
    patient.date_of_birth = data['date_of_birth']
    patient.birth_place = data['birth_place']
    patient.address = data['address']
    patient.contact_no = data['contact_no']

    return jsonify(patient.save())

@module.route('/<patient>', methods=['DELETE'])
def delete(patient):
    patient = Patient().delete(patient)
    return jsonify(patient)