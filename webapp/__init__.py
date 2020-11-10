#!/var/www/cherry-pi-prod/venv

import sys
print(sys.prefix)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_navigation import Navigation
from flask_cors import CORS
import json
from webapp.scripts import test_script, key_64
import datetime

def load_env():
	with open("/var/www/cherry-pi-prod/.env", "r") as fp:
		envs = json.load(fp)
	return envs


env_vars = load_env()

app = Flask(__name__)
app.static_folder = 'static'

app.config['SECRET_KEY'] = env_vars["secret_key"]
app.config['SQLALCHEMY_DATABASE_URI'] = env_vars["postgresql"]

app.jinja_env.globals.update(test=test_script, date=datetime.datetime.now, key64=key_64, dump=json.dumps, int=int, isinstance=isinstance)

cors = CORS(app, resources={r"/js/*": {"origins": "http://silchesterplayers.org"}, r"/listens/*": {"origins": "http://silchesterplayers.org"}})

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
nav = Navigation()
nav.init_app(app)

from webapp import routes

# db.create_all()
