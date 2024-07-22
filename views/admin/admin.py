from flask import Flask, url_for, request, redirect, render_template, Blueprint, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

admin_bp = Blueprint("admin", __name__, template_folder="templates")

@admin_bp.route('/', methods=["GET"])
def admin_index():
    return render_template('admin_index.html')

@admin_bp.route('/signup', methods=["POST", "GET"])
def signup():
    from views.db.db import Admin
    from app import db

    if request.method == "POST":
        form_data = request.form
        email = form_data.get('admin_email')
        name = form_data.get('admin_name')
        password = form_data.get('password')
        # return f"Name: {name}"
        new_admin = Admin(admin_name=name, admin_email=email)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        return "admin added succesfully"
    return jsonify({"error": "unathorized access"}), 403
    # return render_template('admin_signup.html')

@admin_bp.route('/login', methods=["POST", "GET"])
def login():
    from views.db.db import Admin
    error = None
    if request.method == 'POST':
        form_data = request.form
        email = form_data.get('admin_email')
        password = form_data.get('admin_password')

        if not email or not password:
            error = "Email and password are required."
            return render_template("admin_index.html", error=error)
        
        admin_user = Admin.query.filter_by(admin_email=email).first()
        if admin_user and admin_user.check_password(password):
            session.permanent = True
            session['admin_user'] = {"admin_user_id":admin_user.adminid, "email": email, "name": admin_user.admin_name}

            return redirect(url_for('admin.home'))
        else:
            error = "Invalid email or password"
    
    return render_template("admin_index.html", error=error)


@admin_bp.route('/home', methods=["GET", "POST"])
def home():
    if not session.get("admin_user"):
        return redirect(url_for("admin.login"))
    return render_template('admin_home.html')


@admin_bp.route('/dashboard', methods=["GET"])
def dashboard():
    from views.db.db import Users, MedicalHistory, Diseases
    
    users_count = Users.query.count()
    health_data_count = MedicalHistory.query.count()
    diseases_count = Diseases.query.count()
    return render_template('dashboard.html', users_count=users_count, health_data_count=health_data_count, diseases_count=diseases_count)

@admin_bp.route('health-data', methods=["POST", "GET"])
def health_data():
    from views.db.db import MedicalHistory
    admin_user = session.get('admin_user')
    if admin_user:
        try:
            users_medical_history = MedicalHistory.query.order_by(MedicalHistory.diagnosis_date.desc()).all()
            return render_template('health_data.html', medical_history=users_medical_history)
        except OperationalError:
            return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")

    return render_template('admin_index.html')

@admin_bp.route('users', methods=["POST", "GET"])
def users():
    from views.db.db import Users

    users = Users.query.all()

    return render_template('users.html', users=users)

@admin_bp.route('settings', methods=["POST", "GET"])
def settings():
    admin_user = session.get('admin_user')
    if admin_user:
        return render_template('settings.html', admin_user=admin_user)
    return redirect(url_for('admin.login'))

# @admin_bp.route('/save-profile', methods=["POST"])
# def save_profile():
#     from views.db.db import Admin
#     from app import db
#     admin_user = session.get('admin_user')

#     if admin_user:
#         if request.method == "POST":
#             admin_user_id = admin_user.get('admin_user_id')

#             if admin_user_id:
#                 try:
#                     admin_user_obj = Admin.query.filter_by(adminid=admin_user_id).first()
#                     if admin_user_obj:
#                         admin_user_obj.admin_name = request.form.get('username', admin_user_obj.admin_name)
#                         admin_user_obj.admin_email = request.form.get('email', admin_user_obj.admin_email)
#                         db.session.commit()
#                         session.permanent = True
#                         session['update_message'] = "Changes saved successfully."
#                         return redirect(url_for('admin.settings'))
#                     else:
#                         return "Admin user not found.", 404
#                 except OperationalError:
#                     return render_template("error.html", message="Unable to connect to the server. Please check your network connection and try again.")
#             else:
#                 return "No admin ID found.", 400
#         else:
#             return redirect(url_for('admin.login'))
#     return redirect(url_for('admin.login'))



@admin_bp.route('health-diseases', methods=["POST", "GET"])
def health_diseases():
    from views.db.db import Diseases
    try:
        diseases = Diseases.query.all()
    except OperationalError:
            return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")

    return render_template('diseases.html', diseases=diseases)

@admin_bp.route('/api/v1/diseases/<int:disease_id>', methods=['GET'])
def get_disease(disease_id):
    from views.db.db import Diseases
    disease = Diseases.query.get(disease_id)
    if disease:
        return jsonify({
            'disease_id': disease.disease_id,
            'disease_name': disease.disease_name,
            'disease_desc': disease.disease_desc,
            'recommendation_for_disease': disease.recommendation_for_disease
        })
    return jsonify({'error': 'Disease not found'}), 404

@admin_bp.route('/api/v1/diseases/<int:disease_id>', methods=['PUT'])
def update_disease(disease_id):
    from views.db.db import Diseases
    from app import db

    return "You're here"
    disease = Diseases.query.get(disease_id)
    if not disease:
        return jsonify({'error': 'Disease not found'}), 404

    data = request.json
    disease.disease_name = data.get('disease_name')
    disease.disease_desc = data.get('disease_desc')
    disease.recommendation_for_disease = data.get('recommendation_for_disease')
    
    db.session.commit()
    return jsonify({'success': True})

@admin_bp.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    from views.db.db import Users
    from app import db
    try:
        # Find the user by ID
        user = Users.query.get(user_id)
        
        if user is None:
            return jsonify({'message': 'User not found'}), 404
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
    
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@admin_bp.route('/logout', methods=["GET"])
def logout():
    session.pop("admin_user", None)
    return redirect(url_for("admin.admin_index"))
