from sqlalchemy.orm import relationship
from app import db


class Users(db.Model):
    """ The user table
    """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, name, age, gender, email, password):
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.password = password

class Symptoms(db.Model):
    """ The symptoms table
    """
    __tablename__ = 'symptoms'
    symptom_id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(200))
    symptom_desc = db.Column(db.Text())

    def __init__(self, symptom_id, symptom_name, symptom_desc):
        self.symptom_id = symptom_id
        self.symptom_name = symptom_name
        self.symptom_desc = symptom_desc

class Diagnosis(db.Model):
    """ The diagnosis table
    """
    __tablename__ = 'diagnosis'
    diagnosis_id = db.Column(db.Integer, primary_key=True)
    diagnosis_name = db.Column(db.String(200))
    diagnosis_desc = db.Column(db.Text())

    def __init__(self, diagnosis_id, diagnosis_name, diagnosis_desc):
        self.diagnosis_id = diagnosis_id
        self.diagnosis_name = diagnosis_name
        self.diagnosis_desc = diagnosis_desc

class UserDiagnosis(db.Model):
    """ The user_diagnosis table
    """
    __tablename__ = 'user_diagnosis'
    user_diagnosis_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    diagnosis_id = db.Column(db.Integer)
    diagnosis_date = db.Column(db.DateTime)

    user = relationship('Users', backref='user_diagnosis')

    def __init__(self, user_id, diagnosis_id, diagnosis_date):
        self.user_id = user_id
        self.diagnosis_id = diagnosis_id
        self.diagnosis_date = diagnosis_date

class MedicalHistory(db.Model):
    """ The medical_history table
    """
    __tablename__ = 'medical_history'
    medical_history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    diagnosis_id = db.Column(db.Integer)
    diagnosis_date = db.Column(db.DateTime)

    user_id = relationship('Users', backref='medical_history')

    def __init__(self, user_id, diagnosis_id, diagnosis_date):
        self.user_id = user_id
        self.diagnosis_id = diagnosis_id
        self.diagnosis_date = diagnosis_date