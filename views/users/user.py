from flask import Flask, url_for, request, redirect, render_template, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

user_bp = Blueprint("user", __name__, template_folder="templates")


@user_bp.route('/')
def home():
    """ home page of the user
    """
    # return columns
    session.clear()
    return "Hey, I work"
    # return render_template('index.html')

@user_bp.route('/user_input', methods=['GET', 'POST'])
def user_input():
    from views.model.test_csv import columns
    """redirect to the form page"""
    return render_template('symptoms.html', columns=columns)


all_user_symptoms = []
@user_bp.route('/symptoms', methods=['GET', 'POST'])
def symptom():
    """ analyze user symptom to predict the next best question to ask
    """
    if request.method == 'POST':
        user_symptom = request.form.get('symptom')
        # if len(all_user_symptoms) != 7:
        all_user_symptoms.append(user_symptom)
        print(f'You selected {user_symptom}')
        return render_template('intensity.html', symptom_keyword=user_symptom)
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