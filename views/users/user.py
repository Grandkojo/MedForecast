from flask import Flask, url_for, request, redirect, render_template, Blueprint, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy.exc import OperationalError
import numpy as np
import random
from datetime import datetime
user_bp = Blueprint("user", __name__, template_folder="templates", static_folder='static')


@user_bp.route('/')
def home():
    """ home page of the user
    """
    return render_template('index.html')

@user_bp.route('/signup', methods=["GET", "POST"])
def signup():
    from views.db.db import Users
    from app import db

    error = None
    if request.method == "POST":
        form_data = request.form
        email = form_data.get('user_email')
        password = form_data.get('user_password')
        age = form_data.get('user_age')
        gender = form_data.get('gender')
        username = form_data.get('user_name')

        if not email or not password or not username or not gender or not age:
            error = "All fields are required."
            return render_template('signup.html', error=error)
    
        #check if email already exists
        try:
            existing_user = Users.query.filter(Users.email == email).first()
        
            if existing_user:
                if existing_user.email == email:
                    error = "Email already exists, login instead"
            
            else:
                new_user = Users(name=username, age=age, gender=gender, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                session.permanent = True
                session['user'] = {"user_id":new_user.user_id, "email": email, "name": username}
                print(session['user'])
                return redirect(url_for('user.signup_complete'))
            
            return render_template('signup.html', error=error)
        except OperationalError:
            return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
    

    return render_template("signup.html")

@user_bp.route('/login')
def login():
    return render_template('login.html')

@user_bp.route('/signup_complete', methods=["GET"])
def signup_complete():
    user_data = session.get('user')
    if user_data:
        return redirect(url_for('user.home'))
    return redirect(url_for('user.signup'))

@user_bp.route('/medfc-login', methods=["GET", "POST"])
def medfc_login():
    from views.db.db import Users
    user_data = session.get('user')
    if user_data:
        return redirect(url_for('user.home'))
    else:
        error = None
        if request.method == "POST":
            form_data = request.form
            email = form_data.get("user_email")
            password = form_data.get("user_password")

            if not email or not password:
                error = "Email and password are required."
                return render_template("login.html", error=error)

            try:
                user = Users.query.filter_by(email=email).first()
                if user:
                    if user and user.check_password(password):
                        session.permanent = True
                        session['user'] = {"user_id":user.user_id, "email": email, "username": user.name}
                        flash("You were successfully logged in")
                        return redirect(url_for('user.home'))
                    else:
                        error = "Invalid email or password"
                else:
                    error = "No existing email found"
                    return render_template("login.html", error=error)
            except OperationalError:
                return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
        else:
            return render_template("login.html", error=error)
    return render_template('login.html', error=error)

@user_bp.route('/forgot_password', methods=["POST", "GET"])
def forgot_password():
    from views.db.db import Users
    error = None
    if request.method == "POST":
        email = request.form.get("user_email")
        try:
            user = Users.query.filter_by(email=email).first()
            if user:
                if user.email:
                    session["user_email_for_update"] = {"email": user.email}
                    return redirect(url_for('user.update_password'))
                else:
                    error = "Email doesn't exist, please sign up"
            else:
                    error = "Email doesn't exist, please sign up"
        except OperationalError:
            return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
    return render_template('forgot_password.html', error=error)

@user_bp.route('/update_password', methods=["POST", "GET"])
def update_password():
    if request.method == "POST":
        from views.db.db import Users
        from app import db
        error = None
        user_password = request.form.get("user_password")
        confirm_user_password = request.form.get("confirm_user_password")

        if user_password == confirm_user_password:
            email = session["user_email_for_update"].get("email")
            try:
                user = Users.query.filter_by(email=email).first()
                user.set_password(confirm_user_password)
                db.session.commit()
                return redirect(url_for('user.login'))
            except OperationalError:
                return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
        error = "Passwords do not match"
        return render_template("update_password.html", error=error)
    return render_template("update_password.html")


@user_bp.route('/check-health')
def check_health():
    from views.model.test_csv import columns_mappings
    """redirect to the form page"""
    return render_template('symptoms.html', columns_mappings=columns_mappings)

all_user_symptoms = []
@user_bp.route('/symptoms', methods=['GET', 'POST'])
def symptom():
    """ analyze user symptom to predict the next best question to ask
    """
    from src.components.data_ingestion import DataIngestion
    from src.components.model_trainer import ModelTrainer
    from src.utils import get_top_n_features, append_other_feature, calculate_number_of_parameters_to_append
    from views.db.db import Symptoms

    if request.method == 'POST':

        primary_column = request.form.get('symptom')

        obj = DataIngestion()

        data_path = obj.initiate_data_ingestion()

        model_train = ModelTrainer()

        cleaned_data, top_features, accuracy = model_train.initiate_model_trainer(data_path)

        features_from_user, length_of_parameters = get_top_n_features(cleaned_data, primary_column, n=35)

        main_features_to_ask_user = features_from_user

        print(f"features to ask: {len(top_features)}")

        additional_parameter_num = length_of_parameters

        top_features_per_main_symptom = top_features

        session.permanent = True
        session["model_stuff"] = {"features_from_user": features_from_user, "length_of_parameters": length_of_parameters, "top_features": top_features}
        
        try:
            symptoms = Symptoms.query.all()
        except OperationalError:
            return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
        symptom_descriptions = {symptom.symptom_name: symptom.symptom_desc for symptom in symptoms}
        return render_template('symptoms.html', user_specific_questions=top_features, primary_column=primary_column, symptom_descriptions=symptom_descriptions)
    else:
        print(len(all_user_symptoms))
        return render_template('symptoms.html', next_symptom='Enter next symptom')
    

@user_bp.route('/logout', methods=["GET"])
def logout():
    session.pop("user", None)
    return redirect(url_for("user.home"))

@user_bp.route('/process/<string:symptom>', methods=["POST", "GET"])
def process(symptom):
    from views.db.db import Diseases, MedicalHistory
    from src.utils import append_other_feature, calculate_number_of_parameters_to_append, get_top_n_features
    from src.components.data_ingestion import DataIngestion
    from src.components.model_trainer import ModelTrainer
    from app import db

    if request.method == "POST":
        primary_column = symptom
        form_data = request.form
        user_responses = []
        session.permanent = True
        session['form_details'] = dict(form_data.items())

        for _, value in form_data.items():
            if value == "yes":
                user_responses.append(1)
            elif value == "no":
                user_responses.append(0)
        obj = DataIngestion()
        data_path = obj.initiate_data_ingestion()
        model_train = ModelTrainer()
        cleaned_data, top_features, accuracy = model_train.initiate_model_trainer(data_path)
        features_from_user, length_of_parameters = get_top_n_features(cleaned_data, primary_column, n=35)
        cleaned_data, top_features, accuracy = model_train.initiate_model_trainer(data_path)
        num_of_features_to_append = calculate_number_of_parameters_to_append(length_of_parameters)
        other_features_to_append = top_features[:num_of_features_to_append]
        total_features_for_new_training = append_other_feature(top_features[:num_of_features_to_append] , features_from_user)
        new_model, new_accuracy, number_to_choose, total_features = model_train.retrain_model_with_user_input(cleaned_data, total_features_for_new_training)
        user_responses.extend(np.random.choice([0, 1], size=(number_to_choose - len(user_responses))))
        user_responses = [[int(x) for x in user_responses]]
        _, prediction = model_train.predict_with_model(new_model, user_responses, total_features)
        diagnosis = prediction[0]
        print(diagnosis)

        try:
            recommendation = Diseases.query.filter_by(disease_name=diagnosis).first()
            print(recommendation)
            if recommendation is not None:
                brief_description = recommendation.disease_desc
                recommendation_for_disease = recommendation.recommendation_for_disease
            else:
                return "No recommendation found!"
        except OperationalError:
            return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")

        
        user = session.get('user')

        details_of_prediction = {
            "prediction": diagnosis,
            "accuracy": accuracy,
            "description": brief_description,
            "recommendation": recommendation_for_disease
        }

        if user:

            form_details = session.get('form_details')
            form_details['primary_column']= primary_column
            # return form_details
            session.permanent = True
            session['form_details'] = form_details

            try:

                disease = Diseases.query.filter_by(disease_name=details_of_prediction.get('prediction')).first()
                # return f"Disease {disease}"
                disease_id = disease.disease_id
                model_accuracy = round(details_of_prediction.get('accuracy', 0), 2)
                new_medical_record = MedicalHistory(user_id=user.get('user_id'), diagnosis_date=datetime.now(), user_response=form_details, diagnosis_id=disease_id, model_accuracy=model_accuracy)
                db.session.add(new_medical_record)
                db.session.commit()

                return render_template('symptoms.html', details_of_prediction=details_of_prediction, primary_column=primary_column)


            except OperationalError:
                return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
        else:

    
            print(details_of_prediction)

            return render_template('symptoms.html', details_of_prediction=details_of_prediction, primary_column=primary_column)
    return "Fill out the form !!!"

@user_bp.route('/find-care')
def get_location():
    return render_template('get_location.html')

@user_bp.route('/medical-history', methods=["GET"])
def medical_history():
    from views.db.db import MedicalHistory
    user = session.get('user')
    if user:
        user_id = session['user'].get('user_id')
        if user_id:
            try:
                medical_history = MedicalHistory.query.filter_by(user_id=user_id).order_by(MedicalHistory.diagnosis_date.desc()).all()
                return render_template('medical-history.html', medical_history=medical_history)
            except OperationalError:
                return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")

        return "No form details"
    return render_template('login.html')

@user_bp.route('/edit-profile', methods=["GET"])
def edit_profile():
    from views.db.db import Users
    user = session.get('user')
    if user:
        user_id = user.get('user_id')
        if user_id:
            try:
                user = Users.query.get(user_id)
                return render_template('edit_profile.html', user=user)
            except OperationalError:
                return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")

    return redirect(url_for('user.login'))

@user_bp.route('/edit-profile', methods=["POST"])
def save_profile():
    from views.db.db import Users
    from app import db
    user = session.get('user')
    if user:
        user_id = user.get('user_id')
        if user_id:
            try:
                user = Users.query.get(user_id)
                if user:
                    user.name = request.form.get('username')
                    user.email = request.form.get('email')
                    user.age = request.form.get('age')
                    db.session.commit()
                    message = "Changes saved"
                    return render_template('edit_profile.html', message=message)
            except OperationalError:
                return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")

    return redirect(url_for('user.login'))

@user_bp.route('/health-conditions')
def conditions():
    from views.db.db import Diseases
    diseases = Diseases.query.all() 
    return render_template('conditions.html', diseases=diseases)

@user_bp.route('/health-conditions/<int:disease_id>')
def disease_details(disease_id):
    from views.db.db import Diseases, Cause, Treatment
    disease = Diseases.query.get_or_404(disease_id)
    causes = Cause.query.filter_by(disease_id=disease_id).all()
    treatments = Treatment.query.filter_by(disease_id=disease_id).all()
    return render_template('disease_details.html', disease=disease, causes=causes, treatments=treatments)

@user_bp.route('/chat', methods=['POST', 'GET'])
def chat():
    from transformers import GPT2Tokenizer, GPT2LMHeadModel
    if request.method == "POST":
        model_name = "gpt2"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        data = request.get_json()
        user_message = data['message']

        # Tokenize input
        inputs = tokenizer.encode(user_message, return_tensors='pt')

        # Generate response with controlled length and randomness
        outputs = model.generate(
            inputs, 
            max_length=150,   # Limit the length to 150 tokens
            do_sample=True, 
            temperature=0.7,  # Controls creativity (lower for more focused output)
            top_p=0.9,        # Nucleus sampling (lower to filter out less likely tokens)
            pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({"response": response})
    else:
        return render_template('ai-chatbot.html')
