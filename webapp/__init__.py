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
import socket


def load_env():
	hostname = socket.gethostname()
	if hostname == 'DESKTOP-MG5V3KN':
		print("desktop")
		UPLOAD_FOLDER = 'C:/Users/mattl/Documents/repos/cherry-pi/webapp/uploads'
		ROOT_FOLDER = 'C:/Users/mattl/Documents/repos/cherry-pi/webapp'
		with open("C:/Users/mattl/Documents/repos/cherry-pi/.env", "r") as fp:
			envs = json.load(fp)
	elif hostname == 'DESKTOP-RL06TKT':
		print("laptop")
		UPLOAD_FOLDER = '/mnt/c/users/mattl/documents/gitlab/project-cherry-pi/webapp/uploads'
		ROOT_FOLDER = '/mnt/c/users/mattl/documents/gitlab/project-cherry-pi/webapp'
		with open("/mnt/c/users/mattl/documents/gitlab/project-cherry-pi/.env", "r") as fp:
			envs = json.load(fp)
	elif hostname == 'vps6084.first-root.com':
		print("webserver")
		UPLOAD_FOLDER = '/var/www/cherry-pi-prod/webapp/uploads'
		ROOT_FOLDER = '/var/www/cherry-pi-prod/webapp'
		with open("/var/www/cherry-pi-prod/.env", "r") as fp:
			envs = json.load(fp)
	elif hostname == 'BAIN':
		print('testserver')
		UPLOAD_FOLDER = '/home/mattl1598/project-cherry-pi/webapp/uploads'
		ROOT_FOLDER = '/home/mattl1598/project-cherry-pi/webapp'
		with open('/home/mattl1598/project-cherry-pi/.env', "r") as fp:
			envs = json.load(fp)
	else:
		print("other")
		print(hostname)
		raise FileNotFoundError(".env filepath not specified for this host")
	return envs, UPLOAD_FOLDER, ROOT_FOLDER


env_vars, UPLOAD_FOLDER, ROOT_FOLDER = load_env()

app = Flask(__name__)
app.static_folder = 'static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ROOT_FOLDER'] = ROOT_FOLDER

app.config['SECRET_KEY'] = env_vars["secret_key"]
app.config['SQLALCHEMY_DATABASE_URI'] = env_vars["postgresql"]

app.jinja_env.globals.update(test=test_script, date=datetime.datetime.now, key64=key_64, dump=json.dumps, int=int,
								isinstance=isinstance)

cors = CORS(app, resources={r"/js/*": {"origins": "http://silchesterplayers.org"},
							r"/listens/*": {"origins": "http://silchesterplayers.org"},
							r"/soundcounter/*": {"origins": "http://silchesterplayers.org"},
							r"/sp-post*": {"origins": "http://silchesterplayers.org"},
							r"/sp-entry": {"origins": "http://silchesterplayers.org"}
							})

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
nav = Navigation()
nav.init_app(app)

app.env_vars = env_vars

from webapp import routes

# db.create_all()
