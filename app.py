# from flask_cors import CORS
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from views.admin.admin import admin_bp
from views.users.user import user_bp
import views.model
import numpy as np
import joblib
import os

load_dotenv()
app = Flask(__name__)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(user_bp, url_prefix="/user")

app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
supabase_pw = os.environ.get('SUPABASE_PASSWORD')
model = joblib.load('decision_tree_model.pkl')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres.omkdwtvqcnbzazlwvrkd:{supabase_pw}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

db = SQLAlchemy(app)
from views.db.db import *


@app.route('/')
def home():
    """ home page of the app
    """
    # return columns
    session.clear()
    return render_template('index.html')



if __name__ == '__main__':
    from app import app
    from views.db.db import *
    with app.app_context():
        db.create_all()
    app.run()