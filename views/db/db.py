from sqlalchemy.orm import relationship
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    """ The user table """
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Symptoms(db.Model):
    """ The symptoms table """
    __tablename__ = 'symptoms'
    symptom_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symptom_name = db.Column(db.String(200), nullable=False)
    symptom_desc = db.Column(db.Text(), nullable=False)


class Diseases(db.Model):
    """ The diseases table """
    __tablename__ = 'diseases'
    disease_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disease_name = db.Column(db.String(200), unique=True, nullable=False)
    disease_desc = db.Column(db.Text(), nullable=False)
    recommendation_for_disease = db.Column(db.Text(), nullable=False)


class Diagnosis(db.Model):
    """ The diagnosis table """
    __tablename__ = 'diagnosis'
    diagnosis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diagnosis_name = db.Column(db.String(200), nullable=False)
    diagnosis_desc = db.Column(db.Text(), nullable=False)


class UserDiagnosis(db.Model):
    """ The user_diagnosis table """
    __tablename__ = 'user_diagnosis'
    user_diagnosis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.diagnosis_id'), nullable=False)
    diagnosis_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('Users', backref='user_diagnosis')
    diagnosis = db.relationship('Diagnosis', backref='user_diagnosis')


class MedicalHistory(db.Model):
    """ The medical_history table """
    __tablename__ = 'medical_history'
    medical_history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.diagnosis_id'), nullable=False)
    diagnosis_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('Users', backref='medical_history')
    diagnosis = db.relationship('Diagnosis', backref='medical_history')

class Admin(db.Model):
    """ The admin table """
    __tablename__ = 'admin'
    adminid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(200))
    admin_password = db.Column(db.String(200))
    admin_email = db.Column(db.String(200), unique=True)

    def set_password(self, password):
        self.admin_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.admin_password, password)


#need a paid postgresql server/database to run this
# class SymptomData(db.Model):
#     """ A dataset containing symptoms and prognosis
#     """
#     __tablename__ = 'symptom_data'

#     id = db.Column(db.Integer, primary_key=True)
#     itching = db.Column(db.Integer)
#     skin_rash = db.Column(db.Integer)
#     nodal_skin_eruptions = db.Column(db.Integer)
#     continuous_sneezing = db.Column(db.Integer)
#     shivering = db.Column(db.Integer)
#     chills = db.Column(db.Integer)
#     joint_pain = db.Column(db.Integer)
#     stomach_pain = db.Column(db.Integer)
#     acidity = db.Column(db.Integer)
#     ulcers_on_tongue = db.Column(db.Integer)
#     muscle_wasting = db.Column(db.Integer)
#     vomiting = db.Column(db.Integer)
#     burning_micturition = db.Column(db.Integer)
#     spotting_urination = db.Column(db.Integer)
#     fatigue = db.Column(db.Integer)
#     weight_gain = db.Column(db.Integer)
#     anxiety = db.Column(db.Integer)
#     cold_hands_and_feets = db.Column(db.Integer)
#     mood_swings = db.Column(db.Integer)
#     weight_loss = db.Column(db.Integer)
#     restlessness = db.Column(db.Integer)
#     lethargy = db.Column(db.Integer)
#     patches_in_throat = db.Column(db.Integer)
#     irregular_sugar_level = db.Column(db.Integer)
#     cough = db.Column(db.Integer)
#     high_fever = db.Column(db.Integer)
#     sunken_eyes = db.Column(db.Integer)
#     breathlessness = db.Column(db.Integer)
#     sweating = db.Column(db.Integer)
#     dehydration = db.Column(db.Integer)
#     indigestion = db.Column(db.Integer)
#     headache = db.Column(db.Integer)
#     yellowish_skin = db.Column(db.Integer)
#     dark_urine = db.Column(db.Integer)
#     nausea = db.Column(db.Integer)
#     loss_of_appetite = db.Column(db.Integer)
#     pain_behind_the_eyes = db.Column(db.Integer)
#     back_pain = db.Column(db.Integer)
#     constipation = db.Column(db.Integer)
#     abdominal_pain = db.Column(db.Integer)
#     diarrhoea = db.Column(db.Integer)
#     mild_fever = db.Column(db.Integer)
#     yellow_urine = db.Column(db.Integer)
#     yellowing_of_eyes = db.Column(db.Integer)
#     acute_liver_failure = db.Column(db.Integer)
#     fluid_overload_1= db.Column(db.Integer)
#     swelling_of_stomach = db.Column(db.Integer)
#     swelled_lymph_nodes = db.Column(db.Integer)
#     malaise = db.Column(db.Integer)
#     blurred_and_distorted_vision = db.Column(db.Integer)    
#     phlegm = db.Column(db.Integer)
#     throat_irritation = db.Column(db.Integer)
#     redness_of_eyes = db.Column(db.Integer)
#     sinus_pressure = db.Column(db.Integer)
#     runny_nose = db.Column(db.Integer)
#     congestion = db.Column(db.Integer)
#     chest_pain = db.Column(db.Integer)
#     weakness_in_limbs = db.Column(db.Integer)
#     fast_heart_rate = db.Column(db.Integer)
#     pain_during_bowel_movements = db.Column(db.Integer)
#     pain_in_anal_region = db.Column(db.Integer)
#     bloody_stool = db.Column(db.Integer)
#     irritation_in_anus = db.Column(db.Integer)
#     neck_pain = db.Column(db.Integer)
#     dizziness = db.Column(db.Integer)
#     cramps = db.Column(db.Integer)
#     bruising = db.Column(db.Integer)
#     obesity = db.Column(db.Integer)
#     swollen_legs = db.Column(db.Integer)
#     swollen_blood_vessels = db.Column(db.Integer)
#     puffy_face_and_eyes = db.Column(db.Integer)
#     enlarged_thyroid = db.Column(db.Integer)
#     brittle_nails = db.Column(db.Integer)
#     swollen_extremeties = db.Column(db.Integer)
#     excessive_hunger = db.Column(db.Integer)
#     extra_marital_contacts = db.Column(db.Integer)
#     drying_and_tingling_lips = db.Column(db.Integer)
#     slurred_speech = db.Column(db.Integer)
#     knee_pain = db.Column(db.Integer)
#     hip_joint_pain = db.Column(db.Integer)
#     muscle_weakness = db.Column(db.Integer)
#     stiff_neck = db.Column(db.Integer)
#     swelling_joints = db.Column(db.Integer)
#     movement_stiffness = db.Column(db.Integer)
#     spinning_movements = db.Column(db.Integer)
#     loss_of_balance = db.Column(db.Integer)
#     unsteadiness = db.Column(db.Integer)
#     weakness_of_one_body_side = db.Column(db.Integer)
#     loss_of_smell = db.Column(db.Integer)
#     bladder_discomfort = db.Column(db.Integer)
#     foul_smell_of_urine = db.Column(db.Integer)
#     continuous_feel_of_urine = db.Column(db.Integer)
#     passage_of_gases = db.Column(db.Integer)
#     internal_itching = db.Column(db.Integer)
#     toxic_look_typhos = db.Column(db.Integer)
#     depression = db.Column(db.Integer)
#     irritability = db.Column(db.Integer)
#     muscle_pain = db.Column(db.Integer)
#     altered_sensorium = db.Column(db.Integer)
#     red_spots_over_body = db.Column(db.Integer)
#     belly_pain = db.Column(db.Integer)
#     abnormal_menstruation = db.Column(db.Integer)
#     dischromic_patches = db.Column(db.Integer)
#     watering_from_eyes = db.Column(db.Integer)
#     increased_appetite = db.Column(db.Integer)
#     polyuria = db.Column(db.Integer)
#     family_history = db.Column(db.Integer)
#     mucoid_sputum = db.Column(db.Integer)
#     rusty_sputum = db.Column(db.Integer)
#     lack_of_concentration = db.Column(db.Integer)
#     visual_disturbances = db.Column(db.Integer)
#     receiving_blood_transfusion = db.Column(db.Integer)
#     receiving_unsterile_injections = db.Column(db.Integer)
#     coma = db.Column(db.Integer)
#     stomach_bleeding = db.Column(db.Integer)
#     distention_of_abdomen = db.Column(db.Integer)
#     history_of_alcohol_consumption = db.Column(db.Integer)
#     fluid_overload = db.Column(db.Integer)
#     blood_in_sputum = db.Column(db.Integer)
#     prominent_veins_on_calf = db.Column(db.Integer)
#     palpitations = db.Column(db.Integer)
#     painful_walking = db.Column(db.Integer)
#     pus_filled_pimples = db.Column(db.Integer)
#     blackheads = db.Column(db.Integer)
#     scurring = db.Column(db.Integer)
#     skin_peeling = db.Column(db.Integer)
#     silver_like_dusting = db.Column(db.Integer)
#     small_dents_in_nails = db.Column(db.Integer)
#     inflammatory_nails = db.Column(db.Integer)
#     blister = db.Column(db.Integer)
#     red_sore_around_nose = db.Column(db.Integer)
#     yellow_crust_ooze = db.Column(db.Integer)
#     prognosis = db.Column(db.String(200))
