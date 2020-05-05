from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_navigation import Navigation
import json


def load_env():
	with open(".env", "r") as fp:
		envs = json.loads(fp)
	return envs


app = Flask(__name__)


from webapp import routes
