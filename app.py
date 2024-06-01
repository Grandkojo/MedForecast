# from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.debug = True

load_dotenv()
postgres_user = os.environ.get('POSTGRES_USER')
postgres_pw = os.environ.get('POSTGRES_PASSWORD')
postgres_host = os.environ.get('POSTGRES_HOST')
postgres_db = os.environ.get('POSTGRES_DB')


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_pw}@{postgres_host}/{postgres_db}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from db import *


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    from app import app
    from db import *
    with app.app_context():
        db.create_all()
    app.run()