from marshmallow import Schema
from marshmallow.fields import String, Integer, DateTime, Date, Nested
from marshmallow_enum import EnumField

class UserSchema(Schema):
    id = Integer(dump_only=True)
    name = String()
    username = String()
    password = String()
    created_at = DateTime()
    updated_at = DateTime()

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
    created_at = DateTime()
    updated_at = DateTime()
    
class MedicalRecordSchema(Schema):
    id = Integer()
    height = Integer()
    height = String()
    weight = String()
    bmi = String()
    bp = String()
    pr = String()
    temperature = String()
    complaint = String()
    diagnosis = String()
    treatment = String()
    note = String()
    patients = Nested(PatientSchema)
    created_at = DateTime()
    updated_at = DateTime()
