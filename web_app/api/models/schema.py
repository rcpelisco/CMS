from marshmallow import Schema, pre_dump
from marshmallow.fields import String, Integer, DateTime, Date, Nested, Boolean
from marshmallow_enum import EnumField
from custom_enum import Gender, CivilStatus

class UserSchema(Schema):
    id = Integer(dump_only=True)
    name = String()
    username = String()
    password = String()
    slug = String()
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        fields = ('id', 'name', 'username', 'password', 'created_at', 'updated_at')
        ordered=True
        
class MedicalRecordSchema(Schema):
    id = Integer()
    temperature = String()
    complaint = String()
    diagnosis = String()
    treatment = String()
    medical_case = String()
    medical_status = String()
    note = String()
    patient = Nested('PatientSchema', exclude=('medical_records', ))
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')

    class Meta:
        fields = ('id', 'temperature', 'complaint', 'diagnosis', 
            'treatment', 'medical_case', 'medical_status', 'note', 
            'patient', 'created_at', 'updated_at')
        ordered=True

class ReportSchema(Schema):
    medical_case = String()
    count = Integer()

    class Meta:
        fields = ('count', 'medical_case')
        ordered=True

class CategorySchema(Schema):
    category = String()
    medical_status = Nested('ReportSchema', many=True)

class PatientSchema(Schema):
    id = Integer(dump_only=True)
    first_name = String()
    last_name = String()
    gender = EnumField(Gender)
    civil_status = EnumField(CivilStatus)
    height = Integer()
    weight = Integer()
    bmi = String()
    bp = String()
    pr = String()
    date_of_birth = Date()
    birth_place = String()
    address = String()
    contact_no = String()
    slug = String()
    blood_type = String()
    allergy = String()
    emergency_name = String()
    emergency_relation = String()
    emergency_contact = String()
    medical_records = Nested(MedicalRecordSchema, many=True, exclude=('patient', ))
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'gender', 'civil_status', 
            'height', 'weight', 'bmi', 'bp', 'pr', 'date_of_birth', 
            'birth_place', 'address', 'contact_no', 'slug', 'blood_type', 'allergy',
            'emergency_name', 'emergency_relation', 'emergency_contact', 
            'medical_records', 'created_at', 'updated_at')
        ordered=True

class FaceRecognitionSchema(Schema):
    id = Integer()
    name = String()
    fresh = Integer()
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')
        