from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_navigation import Navigation
import json


def load_env():
	with open(".env", "r") as fp:
		envs = json.load(fp)
	return envs


env_vars = load_env()

app = Flask(__name__)
app.static_folder = 'static'

app.config['SECRET_KEY'] = env_vars["secret_key"]
app.config['SQLALCHEMY_DATABASE_URI'] = env_vars["postgresql"]

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
nav = Navigation()
nav.init_app(app)

from webapp import routes
