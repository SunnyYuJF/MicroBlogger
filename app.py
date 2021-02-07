from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '9OLWxND4o83j4K4iuopO')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')


db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)


if __name__ == '__main__':
    app.run()

