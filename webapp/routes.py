from webapp import app, db, nav
from flask import render_template, url_for, request, redirect, session, jsonify, abort
from flask_login import login_user, logout_user, current_user, AnonymousUserMixin, login_required
from webapp.models import User, Post, Sensor, Key, APILog, APIBackup
from webapp.forms import RegistrationForm, LoginForm
import datetime
import base64
import hashlib
import ast

api = {"test": {"name": "test", "number": 420}}


def get_date_time():
	return datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")


def parse_date_time(string1):
	return datetime.datetime.strptime(string1, "%Y-%m-%d_%H-%M-%S")


def gen_nav():
	nav.Bar('guest', [
		nav.Item('Home', 'home'),
		nav.Item('About', 'about'),
		nav.Item('Register', 'register', html_attrs={'class': 'right'}),
		nav.Item('Login', 'login', html_attrs={'class': 'right'}),
		# nav.Item('Logout', 'logout', html_attrs={'class': ["right"]}),
	])

	try:
		print(getattr(current_user, 'firstname'))
		nav.Bar('user', [
			nav.Item('Home', 'home'),
			nav.Item('About', 'about'),
			# nav.Item('Login', 'login', html_attrs={'class': ["right"]}),
			# nav.Item('Register', 'register', html_attrs={'class': ["right"]}),
			nav.Item('Logout', 'logout', html_attrs={'class': 'right'}),
			nav.Item(getattr(current_user, 'firstname'), 'user', html_attrs={'class': 'right'}),
		])
	except AttributeError:
		nav.Bar('user', [
			nav.Item('Home', 'home'),
			nav.Item('About', 'about'),
			# nav.Item('Login', 'login', html_attrs={'class': "right"}),
			# nav.Item('Register', 'register', html_attrs={'class': "right"}),
			nav.Item('Logout', 'logout', html_attrs={'class': 'right'}),
			nav.Item('User', 'user', html_attrs={'class': 'right'})
		])


@app.before_request
def before_request():
	gen_nav()
	session.permanent = True
	app.permanent_session_lifetime = datetime.timedelta(minutes=20)
	session.modified = True


@app.route("/")
@app.route("/home")
def home():
	# posts = Post.query.all()
	# return render_template('home.html', title='Home', posts=posts)
	return render_template('home.html')


@app.route("/about")
def about():
	return render_template('about.html', title="About")


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			user = User.query.filter_by(username=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for('home'))
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return render_template('logged_out.html', title='Logged Out')

@app.route("/admin")
def admin():
	return render_template('admin_page.html', title='Admin Page')

@app.route("/user")
@login_required
def user():
	return render_template('user.html', title='User Settings')


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST':
		id_base = str(form.email.data + form.email.data)
		id = str(base64.urlsafe_b64encode(hashlib.md5(str(id_base).encode('utf-8')).digest()), 'utf-8').rstrip("=")[0:15]
		matches = User.query.filter_by(id=id).paginate().total
		while matches:
			id_base = id_base + "1"
			id = str(base64.urlsafe_b64encode(hashlib.md5(str(id_base).encode('utf-8')).digest()), 'utf-8').rstrip("=")[0:15]
			matches = User.query.filter_by(id=id).paginate().total

		user = User(id=id, firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=form.password.data, role="user")

		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('registered'))
	return render_template('register.html', title='Register', form=form)


@app.route("/registered")
def registered():
	return render_template('registered.html', title='Successfully Registered')


@app.route("/sensor-api/get/<sensor_id>", methods=['GET'])
def sensor_api(sensor_id):
	if (request.method == 'GET') and (Sensor.query.filter_by(id=sensor_id).first is not None):
		if api[sensor_id]:
			return jsonify({"timestamp": get_date_time(), "data": api[sensor_id]})
		else:
			abort(404)


@app.route("/sensor-api/update/", methods=['PUT'])
def api_update():
	if request.method == "PUT":
		data = request.get_json()
		keys = data.keys()
		if "sensor_key" in keys and "data" in keys and "timestamp" in keys and (datetime.datetime.utcnow() - parse_date_time(data["timestamp"])).total_seconds() < 300:
			api_key = Key.query.filter_by(key=data["sensor_key"]).first
			key_type = ast.literal_eval(api_key.type)
			sensor_id = key_type["sensor_id"]
			if Sensor.query.filter_by(id=sensor_id).first.key_id == api_key.id:
				new_log = APILog(datetime=data["timestamp"], sensor_id=sensor_id, dictionary=data["data"])
				db.session.add(new_log)
				for key, value in data.items():
					api[sensor_id][key] = data["data"][key]
		else:
			abort(400)


def make_api_backup():
	new_backup = APIBackup(date=get_date_time(), backup=api)

	db.session.add(new_backup)
	db.session.commit()