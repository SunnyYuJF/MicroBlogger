from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '9OLWxND4o83j4K4iuopO')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

db.init_app(app)


db.create_all()