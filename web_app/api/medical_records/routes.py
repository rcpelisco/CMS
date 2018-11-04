from flask import Blueprint, jsonify, request
from flask_login import current_user
from sqlalchemy.orm import sessionmaker, load_only
from ..models.models import MedicalRecord
from ..models.models import Patient
from ..models.schema import MedicalRecordSchema
from ..models.schema import ReportSchema
from ..models.schema import CategorySchema
from ..models.schema import ComplaintsSchema
from collections import Counter

module = Blueprint('api.medical_records', __name__)

medical_records_schema = MedicalRecordSchema(many=True)
medical_record_schema = MedicalRecordSchema()
report_schema = ReportSchema(many=True)
category_schema = CategorySchema(many=True)
complaints_schema = ComplaintsSchema(many=True)

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
    
    if 'patient_id' in json_data:
        medical_record.patient_id = json_data['patient_id']

    medical_record.bmi = json_data['bmi']
    medical_record.bp = json_data['bp']
    medical_record.pr = json_data['pr']
    medical_record.temperature = json_data['temperature']
    medical_record.height = json_data['height']
    medical_record.weight = json_data['weight']
    medical_record.complaint = json_data['complaint']
    medical_record.diagnosis = json_data['diagnosis']
    medical_record.note = json_data['note']
    medical_record.treatment = json_data['treatment']
    medical_record.medical_status = json_data['medical_status']
    medical_record.user_id = current_user.id
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

@module.route('/report/<complaint>', methods=['GET'])
def complaint(complaint):
    query = MedicalRecord().get_complaint(complaint)
    if query is None:
        return jsonify({'message': 'Complaint not found!'}), 400
    dump, errors = complaints_schema.dump(query, many=True)
    return jsonify({ 'medical_record': dump })

@module.route('/report', methods=['GET'])
def report():
    query = MedicalRecord().report()
    status = [
        {'category': 'EENT', 'medical_status': [
            {'complaint': 'nose bleeding', 'count': 0},
            {'complaint': 'redness of eye', 'count': 0},
            {'complaint': 'lip bleeding', 'count': 0}
        ]},
        {'category': 'CARDIO VASCULAR', 'medical_status': [
            {'complaint': 'chest pain', 'count': 0}
        ]},
        {'category': 'RESPIRATORY', 'medical_status': [
            {'complaint': 'colds', 'count': 0},
            {'complaint': 'cough', 'count': 0}
        ]},
        {'category': 'GASTROINTESTINAL', 'medical_status': [
            {'complaint': 'hyperacidity', 'count': 0},
            {'complaint': 'LBM', 'count': 0},
            {'complaint': 'stomachache', 'count': 0},
            {'complaint': 'vomiting', 'count': 0}
        ]},
        {'category': 'MUSCULOSKELETAL', 'medical_status': [
            {'complaint': 'body malaise', 'count': 0},
            {'complaint': 'muscle pain', 'count': 0}
        ]},
        {'category': 'DERMA', 'medical_status': [
            {'complaint': 'hypersensitivity', 'count': 0},
            {'complaint': 'insect bite', 'count': 0},
            {'complaint': 'blisters', 'count': 0}
        ]},
        {'category': 'SURGICAL', 'medical_status': [
            {'complaint': 'abrasion', 'count': 0}
        ]},
        {'category': 'DENTAL', 'medical_status': [
            {'complaint': 'toothache', 'count': 0},
            {'complaint': 'consultations', 'count': 0}
        ]},
        {'category': 'NEUROLOGICAL', 'medical_status': [
            {'complaint': 'dizziness', 'count': 0},
            {'complaint': 'fever', 'count': 0},
            {'complaint': 'headache', 'count': 0}
        ]},
        {'category': 'REPRODUCTIVE', 'medical_status': [
            {'complaint': 'dysmenorrhea', 'count': 0}
        ]},
        {'category': 'MISCELLANEOUS', 'medical_status': [
            {'complaint': 'BP TAKING', 'count': 0},
            {'complaint': 'OTHER CONSULTATIONS', 'count': 0}
        ]}
    ]
    

    for count, complaint in query:
        for category in status:
            for item in category['medical_status']:
                if item['complaint'] == complaint:
                    item['count'] = count
                    break

    dump, errors = category_schema.dump(status, many=True)
    return jsonify({'medical_report': dump})
