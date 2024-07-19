# from flask_cors import CORS
from flask import Flask, request, jsonify, render_template, session, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
# from views.admin.admin import admin_bp
# from views.users.user import user_bp
from datetime import timedelta
from transformers import GPT4Model, GPT4Tokenizer


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

# app.register_blueprint(admin_bp, url_prefix="/admin")
# app.register_blueprint(user_bp)

db = SQLAlchemy(app)

# Load pre-trained model and tokenizer
model = GPT4Model.from_pretrained('gpt-4')
tokenizer = GPT4Tokenizer.from_pretrained('gpt-4')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')

    # Tokenize and generate response
    inputs = tokenizer.encode(user_input, return_tensors='pt')
    outputs = model.generate(inputs, max_length=500, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({'response': response})


if __name__ == '__main__':
    from app import app
    from views.db.db import *
    with app.app_context():
        db.create_all()
    app.run()