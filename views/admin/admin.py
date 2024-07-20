from flask import Flask, url_for, request, redirect, render_template, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
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

@admin_bp.route('/dashboard', methods=["GET"])
def dashboard():
    return render_template('dashboard.html')

@admin_bp.route('health-data', methods=["POST", "GET"])
def health_data():
    return "You're health data"

@admin_bp.route('users', methods=["POST", "GET"])
def users():
    from views.db.db import Users

    users = Users.query.all()

    return render_template('users.html', users=users)

@admin_bp.route('settings', methods=["POST", "GET"])
def settings():
    return "You're settings"

@admin_bp.route('health-diseases', methods=["POST", "GET"])
def health_diseases():
    from views.db.db import Diseases

    diseases = Diseases.query.all()

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

    disease = Diseases.query.get(disease_id)
    if not disease:
        return jsonify({'error': 'Disease not found'}), 404

    data = request.form
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