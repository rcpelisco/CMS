from marshmallow import Schema, pre_dump
from marshmallow.fields import String, Integer, DateTime, Date, Nested, Boolean
from marshmallow_enum import EnumField
from custom_enum import Gender, CivilStatus


class MedicalRecordSchema(Schema):
    id = Integer()
    complaint = String()
    diagnosis = String()
    treatment = String()
    medical_status = String()
    note = String()
    height = Integer()
    weight = Integer()
    bmi = String()
    bp = String()
    pr = String()
    temperature = String()
    patient = Nested('PatientSchema', exclude=('medical_records', ))
    user = Nested('UserSchema')
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')

    class Meta:
        fields = ('id', 'complaint', 'diagnosis', 'height', 'weight', 
            'bmi', 'bp', 'pr', 'temperature', 'treatment', 'medical_status', 
            'note', 'patient', 'user', 'created_at', 'updated_at')
        ordered=True

class UserSchema(Schema):
    id = Integer(dump_only=True)
    name = String()
    username = String()
    password = String()
    profile_picture_path = String()
    slug = String()
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        fields = ('id', 'name', 'username', 'password', 'created_at', 'updated_at', 'profile_picture_path')
        ordered=True

class ReportSchema(Schema):
    complaint = String()
    count = Integer()

    class Meta:
        fields = ('count', 'complaint')
        ordered=True

class ComplaintsSchema(Schema):
    class Meta:
        fields = ('medical_record_id', 'complaint', 'alias', 'created_at')
        orderd = True

class CategorySchema(Schema):
    category = String()
    medical_status = Nested('ReportSchema', many=True)

class PatientSchema(Schema):
    id = Integer(dump_only=True)
    first_name = String()
    last_name = String()
    gender = EnumField(Gender)
    civil_status = EnumField(CivilStatus)
    date_of_birth = Date()
    birth_place = String()
    address = String()
    contact_no = String()
    alias = String()
    slug = String()
    blood_type = String()
    allergy = String()
    emergency_name = String()
    emergency_relation = String()
    emergency_contact = String()
    profile_picture_path = String()
    medical_records = Nested(MedicalRecordSchema, many=True, exclude=('patient', ))
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'gender', 'civil_status', 'date_of_birth', 
            'birth_place', 'address', 'contact_no', 'alias', 'slug', 'blood_type', 'allergy',
            'emergency_name', 'emergency_relation', 'emergency_contact', 'profile_picture_path',
            'medical_records', 'created_at', 'updated_at')
        ordered=True

class FaceRecognitionSchema(Schema):
    id = Integer()
    name = String()
    fresh = Integer()
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')
        