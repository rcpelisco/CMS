from marshmallow import Schema, pre_dump
from marshmallow.fields import String, Integer, DateTime, Date, Nested
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
    height = Integer()
    weight = Integer()
    bmi = String()
    bp = String()
    pr = String()
    temperature = String()
    complaint = String()
    diagnosis = String()
    treatment = String()
    medical_status = String()
    note = String()
    patient = Nested('PatientSchema', exclude=('medical_records', ))
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')

    class Meta:
        fields = ('id', 'height', 'weight', 'bmi', 'bp', 'pr', 'temperature', 'complaint', 
            'diagnosis', 'treatment', 'medical_status', 'note', 'patient', 'created_at', 'updated_at')
        ordered=True

class ReportSchema(Schema):
    name = String()
    count = Integer()

    class Meta:
        fields = ('count', 'name')
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
    date_of_birth = Date()
    birth_place = String()
    address = String()
    contact_no = String()
    slug = String()
    medical_records = Nested(MedicalRecordSchema, many=True, exclude=('patient', ))
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'gender', 'civil_status', 
            'date_of_birth', 'birth_place', 'address', 
            'contact_no', 'slug', 'medical_records', 'created_at', 'updated_at')
        ordered=True

class FaceRecognitionSchema(Schema):
    id = Integer()
    name = String()
    created_at = DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = DateTime('%Y-%m-%d %H:%M:%S')
        