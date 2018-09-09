from ...extension import db
from mixins import BasicMixin
from custom_enum import Gender, CivilStatus

class User(BasicMixin, db.Model):
    __tablename__ = 'users'

    name = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(191), nullable=False)

class Patient(BasicMixin, db.Model):
    __tablename__ = 'patients'

    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    civil_status = db.Column(db.Enum(CivilStatus), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    birth_place = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(125), nullable=False)
    contact_no = db.Column(db.String(20), nullable=False)
    medical_records = db.relationship("MedicalRecord", back_populates="patient",
         cascade="all, delete-orphan")

class MedicalRecord(BasicMixin, db.Model):
    __tablename__ = 'medical_records'

    height = db.Column(db.DECIMAL(5, 2), nullable=False)
    weight = db.Column(db.DECIMAL(5, 2), nullable=False)
    bmi = db.Column(db.DECIMAL(5, 2), nullable=False)
    bp = db.Column(db.String(20), nullable=False)
    pr = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.DECIMAL(5, 2), nullable=False)
    complaint = db.Column(db.String(45), nullable=False)
    diagnosis = db.Column(db.String(45), nullable=False)
    treatment = db.Column(db.String(45), nullable=False)
    note = db.Column(db.String(191))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient = db.relationship('Patient', back_populates='medical_records')
