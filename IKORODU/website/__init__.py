from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Reddington:iloveJesus@1@localhost/ikd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ikorodu.db'


db = SQLAlchemy(app)


from .models import User


login_manager = LoginManager()
login_manager.login_view = 'auth'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from website import routes