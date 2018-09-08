from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from ..models.medical_record import MedicalRecord, MedicalRecordSchema

module = Blueprint('api.medical_records', __name__)

medical_records_schema = MedicalRecordSchema(many=True)
medical_record_schema = MedicalRecordSchema()

@module.route('/', methods=['GET'])
def index():
    medical_records = MedicalRecord.query.all()
    medical_records, errors = medical_records_schema.dump(medical_records, many=True)
    return jsonify({'medical_records': medical_records})

@module.route('/<medical_record>', methods=['GET'])
def show(medical_record):
    medical_record = MedicalRecord.query.get(medical_record)
    if medical_record is None:
        return jsonify({'message': 'Medical record not found!'}), 400
    medical_record, errors = medical_records_schema.dump(medical_record)
    return jsonify({'medical_record': medical_record})
    
@module.route('/', methods=['PUT', 'POST'])
def store():
    json_data = request.get_json()
    medical_record = MedicalRecord()
    message = 'Medical record created'
    
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    if 'id' in json_data:
        medical_record = MedicalRecord.query.get(json_data['id'])

    if medical_record is None:
        return jsonify({'message': 'Medical record not found!'}), 400
    
    patient.first_name = json_data['first_name']
    patient.last_name = json_data['last_name']
    patient.gender = json_data['gender']
    patient.civil_status = json_data['civil_status']
    patient.date_of_birth = json_data['date_of_birth']
    patient.birth_place = json_data['birth_place']
    patient.address = json_data['address']
    patient.contact_no = json_data['contact_no']
    patient.save()

    patient_result, errors = patient_schema.dump(medical_record)

    return jsonify({'message': message, 'user': patient_result})

@module.route('/<medical_record>', methods=['DELETE'])
def delete(medical_record):
    patient = Patient.query.get(medical_record)
    if patient is None:
        return jsonify({'message': 'Patient not found!'}), 400
    patient_result, errors = patient_schema.dump(medical_record)
    patient_session = sessionmaker().object_session(medical_record)
    patient_session.delete(medical_record)
    patient_session.commit()
    return jsonify({'message': 'User deleted', 'patient': patient_result})