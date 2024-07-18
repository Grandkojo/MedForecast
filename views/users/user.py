from flask import Flask, url_for, request, redirect, render_template, Blueprint, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy.exc import OperationalError
import numpy as np

user_bp = Blueprint("user", __name__, template_folder="templates", static_folder='static')


@user_bp.route('/')
def home():
    """ home page of the user
    """
    # return columns
    # session.clear()
    # return "Hey, I work"
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
            if user and user.check_password(password):
                session.permanent = True
                session['user'] = {"user_id":user.userid, "email": email, "username": user.username}
                # return jsonify({"user": session['user']})
                flash("You were successfully logged in")
                return redirect(url_for('user.home'))
            else:
                error = "Invalid email or password"
        except OperationalError:
            return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
    
    return render_template("login.html", error=error)

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
    return "Yay, wanna check your health?"


@user_bp.route('/user_input', methods=['GET', 'POST'])
def user_input():
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

    if request.method == 'POST':
        primary_column = request.form.get('symptom')

        obj = DataIngestion()
        data_path = obj.initiate_data_ingestion()

        model_train = ModelTrainer()

        cleaned_data, top_features, accuracy = model_train.initiate_model_trainer(data_path)

        features_from_user, length_of_parameters = get_top_n_features(cleaned_data, primary_column, n=35)

        main_features_to_ask_user = features_from_user

        print(f"features to ask: {len(main_features_to_ask_user)}")

        additional_parameter_num = length_of_parameters
        top_features_per_main_symptom = top_features

        session.permanent = True
        session["model_stuff"] = {"features_from_user": features_from_user, "length_of_parameters": length_of_parameters, "top_features": top_features}

        return render_template('symptoms.html', user_specific_questions=main_features_to_ask_user, primary_column=primary_column)


        num_of_features_to_append = calculate_number_of_parameters_to_append(length_of_parameters)

        other_features_to_append = top_features[:num_of_features_to_append]

        total_features_for_new_training = append_other_feature(top_features[:num_of_features_to_append] , features_from_user)
        
        new_model, new_accuracy, number_to_choose, total_features = model_train.retrain_model_with_user_input(cleaned_data, total_features_for_new_training)


        # print(f"Features to ask the user {features_from_user}, number {len(features_from_user)}")
        print(f"accuracy: {new_accuracy}, number: {number_to_choose}")

        user_responses = np.random.choice([0, 1], size=(1, number_to_choose))


        prediction, _ = model_train.predict_with_model(new_model, user_responses, total_features)

        print(prediction)
        
        print(f"features to ask: {len(features_from_user)}")
        return render_template('symptoms.html', user_specific_questions=features_from_user)
        return "Yes"
        # if len(all_user_symptoms) != 7:
        # all_user_symptoms.append(user_symptom)
        # print(f'You selected {user_symptom}')
        # return render_template('intensity.html', symptom_keyword=user_symptom)
    else:
            # return f'You selected {all_user_symptoms}'
        print(len(all_user_symptoms))
        return render_template('symptoms.html', next_symptom='Enter next symptom')
    
    # if request.method == 'POST':
    #     user_symptoms = request.form.getlist('symptoms')
    #     print(user_symptoms)
    #     exit(0)
    #     session['responses'] = user_symptoms

    #     if len(session['responses']) < 7:
    #         next_symptom = predict_nest_Symptom(session['responses'])
    #         return redirect(url_for('symptoms.html', next_symptom=next_symptom))
    #     else:
    #         prognosis = model.predict([session['responses']])
    #         return render_template('result.html', prognosis=prognosis)
    # else:
    #     session['responses'] = []
    #     nest_symptom = predict_next_symptom([])
    #     return render_template('symptoms.html', next_symptom=next_symptom)
    

@user_bp.route('/process/<string:symptom>', methods=["POST", "GET"])
def process(symptom):
    from src.utils import append_other_feature, calculate_number_of_parameters_to_append, get_top_n_features
    from src.components.data_ingestion import DataIngestion
    from src.components.model_trainer import ModelTrainer

    # if session.get("model_stuff"):
    #     top_features = session["model_stuff"].get('top_features')
    #     length_of_parameters = session["model_stuff"].get('length_of_parameters')
    #     features_from_user = session["model_stuff"].get('features_from_user')
    # else:
    #     return "Session not found"

    if request.method == "POST":
        
        primary_column = symptom

        form_data = request.form

        user_responses = []

        for _, value in form_data.items():
            if value == "yes":
                user_responses.append('1')
            elif value == "no":
                user_responses.append('0')

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

        user_responses.extend(np.random.choice([0, 1], size=(number_to_choose - len(user_responses))).tolist())

        # return f"{user_responses}, length: {len(user_responses)}"
        # return user_responses
    
        prediction, _ = model_train.predict_with_model(new_model, user_responses, total_features)

        return f"Prediction: {prediction}, accuracy: {accuracy}"

    return "Fill out the form !!!"

@user_bp.route('/intensity/<symptom_keyword>', methods=['POST', 'GET'])
def intensity(symptom_keyword):
    """ get user intensity of the symptom"""
    if request.method == "POST":
        intensity = request.form.get('intensity')
        print(f'You selected {intensity}')
        return render_template('repetition.html', symptom_keyword=symptom_keyword)
    else:
        return 'Wrong'
        # if intensity == 'getting_better':
        #     """logic to process"""
        #     pass
        # elif intensity == 'staying_the_same':
        #     """logic to process"""
        #     pass
        # elif intensity == 'getting_worse':
        #     """logic to process"""
        #     pass
        # return 'Choose a right one!'


@user_bp.route('/repetition/<symptom_keyword>', methods=['POST', 'GET'])
def repetition(symptom_keyword):
    """ how often does the symptom occur"""
    if not request.method == 'POST':
        return 'Wrong'
    
    # print(symptom_keyword)
    repetition = request.form.get('repetition')
    print(f'You selected {repetition}')
    
    if repetition == 'constant':
        """logic to process"""
        pass
    elif repetition == 'come_and_go':
        """logic to process"""
        pass
    # return 'Choose a right one!'
    return render_template('severity.html', symptom_keyword=symptom_keyword)


@user_bp.route('/severity/<symptom_keyword>', methods=['POST', 'GET'])
def severity(symptom_keyword):
    """ how severe is the symptom"""
    if not request.method == 'POST':
        return 'Wrong'
    
    severity = request.form.get('severity')
    print(f'You selected {severity}')
    
    if severity == 'mild':
        """logic to process"""
        pass
    elif severity == 'moderate':
        """logic to process"""
        pass
    elif severity == 'severe':
        """logic to process"""
        pass
    # return 'Choose a right one!'
    return render_template('duration.html', symptom_keyword=symptom_keyword)

def predict_next_symptom():
    """logic to determine the next symptoms to ask the user
    """
    pass