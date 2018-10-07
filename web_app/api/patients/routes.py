from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from ..models.models import Patient
from ..models.schema import PatientSchema

module = Blueprint('api.patients', __name__)

patients_schema = PatientSchema(many=True)
patient_schema = PatientSchema()

@module.route('/', methods=['GET'])
def index():
    patients = Patient.query.all()
    patient_results, errors = patients_schema.dump(patients, many=True)
    return jsonify({'patients': patient_results})

@module.route('/<patient>', methods=['GET'])
def show(patient):
    patient = Patient.query.get(patient)
    if patient is None:
        return jsonify({'message': 'Patient not found!'}), 400
    patient_result, errors = patient_schema.dump(patient)
    return jsonify({'patient': patient_result})
    
@module.route('/', methods=['PUT', 'POST'])
def store():
    json_data = request.get_json()
    patient = Patient()
    message = 'Patient created'
    
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    if 'id' in json_data:
        message = 'Patient updated'
        patient = Patient.query.get(json_data['id'])

    if patient is None:
        return jsonify({'message': 'Patient not found!'}), 400
    
    print(json_data)

    patient.first_name = json_data['first_name']
    patient.last_name = json_data['last_name']
    patient.gender = json_data['gender']
    patient.civil_status = json_data['civil_status']
    patient.date_of_birth = json_data['date_of_birth']
    patient.birth_place = json_data['birth_place']
    patient.address = json_data['address']
    patient.contact_no = json_data['contact_no']
    patient.bmi = json_data['bmi']
    patient.bp = json_data['bp']
    patient.height = json_data['height']
    patient.pr = json_data['pr']
    patient.weight = json_data['weight']
    patient.blood_type = json_data['blood_type']
    patient.allergy = json_data['allergy']
    patient.emergency_name = json_data['emergency_name']
    patient.emergency_contact = json_data['emergency_contact']
    patient.emergency_relation = json_data['emergency_relation']
    slug = patient.first_name + ' ' + patient.last_name
    patient.slug = slug.replace(' ', '-').lower()
    patient.save()

    patient_result, errors = patient_schema.dump(patient)

    return jsonify({'message': message, 'patient': patient_result})

@module.route('/<patient>', methods=['DELETE'])
def delete(patient):
    patient = Patient.query.get(patient)
    if patient is None:
        return jsonify({'message': 'Patient not found!'}), 400
    patient_result, errors = patient_schema.dump(patient)
    patient_session = sessionmaker().object_session(patient)
    patient_session.delete(patient)
    patient_session.commit()
    return jsonify({'message': 'User deleted', 'patient': patient_result})
