#!/var/www/cherry-pi-prod/venv

from datetime import datetime
from webapp import db
from webapp import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


def get_date_time():
	return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


class Key(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	key = db.Column(db.String(64))
	type = db.Column(db.Text)
	sensor = db.relationship('Sensor', backref='key', lazy=True, uselist=False)

	def __repr__(self):
		return f"Key('{self.key}', '{self.type}')"


class Sensor(db.Model):
	id = db.Column(db.String(16), primary_key=True)
	name = db.Column(db.String(40), nullable=False)
	key_id = db.Column(db.Integer, db.ForeignKey('key.id'))
	desc = db.Column(db.Text)

	def __repr__(self):
		return f"Sensor('{self.name}', '{self.key_id}', '{self.desc}'"


class APIBackup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=get_date_time)
	backup = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"APIBackup('{self.id}', '{self.date}', '{self.backup}')"


class APILog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=get_date_time)
	sensor_id = db.Column(db.String(64))
	dictionary = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"APILog('{self.date}', '{self.sensor_id}', '{self.dictionary}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	title = db.Column(db.Text, nullable=False)
	category = db.Column(db.Text, nullable=False)
	content = db.Column(db.Text, nullable=False)
	image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
	author_id = db.Column(db.String(16), db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.date}', '{self.title}', '{self.content}', '{self.category}', '{self.image_file}', '{self.author_id}')"


def now():
	return datetime.utcnow().strftime()


class SPPost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=now)
	title = db.Column(db.Text, nullable=False)
	category = db.Column(db.Text, nullable=False)
	content = db.Column(db.Text, nullable=False)
	author = db.Column(db.String(40))

	def __repr__(self):
		return f"SPPost('{self.id}', '{self.date}', '{self.title}', '{self.category}', '{self.content}', '{self.author}')"

	def get_dict(self):
		post_dict = {
			"id": self.id,
			"date": self.date,
			"title": self.title,
			"category": self.category,
			"content": self.content,
			"author": self.author
		}
		return post_dict


class SPCode(db.Model):
	id = db.Column(db.String(16), primary_key=True)
	char = db.Column(db.String(64), nullable=False)
	session = db.Column(db.String(64), nullable=False)
	active = db.Column(db.String(5), nullable=False)

	def __repr__(self):
		return f"SPCode('{self.id}', '{self.char}', '{self.active}')"


class User(UserMixin, db.Model):
	id = db.Column(db.String(16), primary_key=True)
	username = db.Column(db.String(15), unique=True, nullable=False)
	firstname = db.Column(db.String(20), nullable=False)
	lastname = db.Column(db.String(30))
	email = db.Column(db.String(120), unique=True, nullable=False)
	role = db.Column(db.String(40), nullable=False)
	password_hash = db.Column(db.String(128))
	password = db.Column(db.String(60), nullable=False)
	post = db.relationship('Post', backref='user', lazy=True)

	def __repr__(self):
		return f"User('{self.id}', '{self.firstname}', '{self.lastname}', '{self.username}', '{self.role}', '{self.email}')"

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(str(user_id))
