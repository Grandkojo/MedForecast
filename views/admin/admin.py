from flask import Flask, url_for, request, redirect, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

admin_bp = Blueprint("admin", __name__, template_folder="templates")