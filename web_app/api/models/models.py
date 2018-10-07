from ...extension import db, login_manager
from flask_login import UserMixin
from mixins import BasicMixin
from custom_enum import Gender, CivilStatus
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(191), nullable=False)
    slug = db.Column(db.String(90), nullable=False)
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp(), 
        onupdate=func.current_timestamp())

    def save(self):
        if self.id is None:
            db.session.add(self)
        db.session.commit()

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
    height = db.Column(db.DECIMAL(5, 2), nullable=False)
    weight = db.Column(db.DECIMAL(5, 2), nullable=False)
    bmi = db.Column(db.DECIMAL(5, 2), nullable=False)
    bp = db.Column(db.String(20), nullable=False)
    pr = db.Column(db.String(20), nullable=False)
    slug = db.Column(db.String(90), nullable=False)
    medical_records = db.relationship("MedicalRecord", back_populates="patient",
         cascade="all, delete-orphan")

class MedicalRecord(BasicMixin, db.Model):
    __tablename__ = 'medical_records'

    temperature = db.Column(db.DECIMAL(5, 2), nullable=False)
    complaint = db.Column(db.String(45), nullable=False)
    diagnosis = db.Column(db.String(45), nullable=False)
    treatment = db.Column(db.String(45), nullable=False)
    medical_status = db.Column(db.String(191), nullable=False)
    medical_case = db.Column(db.String(191), nullable=False)
    note = db.Column(db.String(191))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient = db.relationship('Patient', back_populates='medical_records')

    def report(self):
        query = db.engine.execute('SELECT COUNT(`medical_case`) as `count`, `medical_case` as `name` FROM `medical_records` GROUP BY `medical_case`')
        return query

class FaceRecognition(BasicMixin, db.Model):
    __tablename__ = 'face_recognition'

    name = db.Column(db.String(30), nullable=False)
    fresh = db.Column(db.Integer)