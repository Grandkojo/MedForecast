# from flask_cors import CORS
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from views.admin.admin import admin_bp
from views.users.user import user_bp
from datetime import timedelta

# import views.model
import numpy as np
import joblib
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

# model = joblib.load('decision_tree_model.pkl')

app.config['CACHE_TYPE'] = 'simple'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)
app.debug = True

app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(user_bp)

db = SQLAlchemy(app)


if __name__ == '__main__':
    from app import app
    from views.db.db import *
    with app.app_context():
        db.create_all()
    app.run()