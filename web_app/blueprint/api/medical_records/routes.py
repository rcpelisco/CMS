from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from ..models.models import MedicalRecord
from ..models.schema import MedicalRecordSchema

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
    medical_record, errors = medical_record_schema.dump(medical_record)
    return jsonify({'medical_record': medical_record})
    
@module.route('/', methods=['PUT', 'POST'])
def store():
    json_data = request.get_json()
    medical_record = MedicalRecord()
    message = 'Medical record created'
    
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    if 'id' in json_data:
        message = 'Medical record updated'
        medical_record = MedicalRecord.query.get(json_data['id'])

    if medical_record is None:
        return jsonify({'message': 'Medical record not found!'}), 400
    
    medical_record.bmi = json_data['bmi']
    medical_record.bp = json_data['bp']
    medical_record.complaint = json_data['complaint']
    medical_record.diagnosis = json_data['diagnosis']
    medical_record.height = json_data['height']
    medical_record.note = json_data['note']
    medical_record.pr = json_data['pr']
    medical_record.temperature = json_data['temperature']
    medical_record.treatment = json_data['treatment']
    medical_record.weight = json_data['weight']
    medical_record.patient_id = json_data['patient_id']
    medical_record.save()

    medical_record, errors = medical_record_schema.dump(medical_record)

    return jsonify({'message': message, 'medical_record': medical_record})

@module.route('/<medical_record>', methods=['DELETE'])
def delete(medical_record):
    query = MedicalRecord.query.get(medical_record)
    if MedicalRecord is None:
        return jsonify({'message': 'MedicalRecord not found!'}), 400
    dump, errors = medical_record_schema.dump(query)
    session = sessionmaker().object_session(query)
    session.delete(query)
    session.commit()
    return jsonify({'message': 'Medical record deleted', 'medical_record': dump})
