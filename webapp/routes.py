from webapp import app, db, nav
from flask import render_template, url_for, request, redirect, session, jsonify, abort, Response
from flask_login import login_user, logout_user, current_user, AnonymousUserMixin, login_required
from webapp.models import User, Post, Sensor, Key, APILog, APIBackup, get_date_time
from webapp.forms import RegistrationForm, LoginForm
from webapp.scripts import key_64, nested_keys
import datetime
import base64
import hashlib
import ast
import json

api = {"test": {"name": "test", "number": 420}}


def parse_date_time(string1):
	return datetime.datetime.strptime(string1, "%Y-%m-%d_%H-%M-%S")


def gen_nav():
	nav.Bar('guest', [
		nav.Item('Home', 'home'),
		nav.Item('Sensors', 'sensors'),
		nav.Item('About', 'about'),
		nav.Item('Register', 'register', html_attrs={'class': 'right'}),
		nav.Item('Login', 'login', html_attrs={'class': 'right'}),
		# nav.Item('Logout', 'logout', html_attrs={'class': ["right"]}),
	])

	try:
		nav.Bar('user', [
			nav.Item('Home', 'home'),
			nav.Item('Sensors', 'sensors'),
			nav.Item('About', 'about'),
			# nav.Item('Login', 'login', html_attrs={'class': ["right"]}),
			# nav.Item('Register', 'register', html_attrs={'class': ["right"]}),
			nav.Item('Logout', 'logout', html_attrs={'class': 'right'}),
			nav.Item(getattr(current_user, 'firstname'), 'user', html_attrs={'class': 'right'}),
		])
	except AttributeError:
		nav.Bar('user', [
			nav.Item('Home', 'home'),
			nav.Item('Sensors', 'sensors'),
			nav.Item('About', 'about'),
			# nav.Item('Login', 'login', html_attrs={'class': "right"}),
			# nav.Item('Register', 'register', html_attrs={'class': "right"}),
			nav.Item('Logout', 'logout', html_attrs={'class': 'right'}),
			nav.Item('User', 'user', html_attrs={'class': 'right'})
		])

	try:
		nav.Bar('admin', [
			nav.Item('Home', 'home'),
			nav.Item('Sensors', 'sensors'),
			nav.Item('Admin', 'admin'),
			nav.Item('About', 'about'),
			# nav.Item('Login', 'login', html_attrs={'class': ["right"]}),
			# nav.Item('Register', 'register', html_attrs={'class': ["right"]}),
			nav.Item('Logout', 'logout', html_attrs={'class': 'right'}),
			nav.Item(getattr(current_user, 'firstname'), 'user', html_attrs={'class': 'right'}),
		])
	except AttributeError:
		nav.Bar('admin', [
			nav.Item('Home', 'home'),
			nav.Item('Sensors', 'sensors'),
			nav.Item('Admin', 'admin'),
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


@app.route("/bse64/<int:length>", methods=['GET'])
def bse_64(length):
	return jsonify({"key": key_64(length)})


@app.route("/about")
def about():
	return render_template('about.html', title="About")


@app.route("/sensors")
def sensors():
	sensor_list = Sensor.query.all()
	sensor_dict = {}
	for sensor in sensor_list:
		desc = ast.literal_eval(sensor.desc)
		desc.update({"id": sensor.id, "name": sensor.name})
		sensor_dict[str(sensor.id)] = desc
	print(sensor_dict)
	return render_template('sensors.html', title="Sensors", sensors=sensor_dict)


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
	try:
		if "admin" != current_user.role:
			abort(403)
		else:
			return render_template('admin_page.html', title='Admin Page')
	except AttributeError:
		abort(403)


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

		new_user = User(id=id, firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=form.password.data, role="user")

		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)
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
		if "time_stamp" in keys and "sensor_id" in keys and "data" in keys and "verification" in keys:
			sensor_id = data["sensor_id"]
			sensor_db = Sensor.query.filter_by(id=sensor_id).first()
			api_key = Key.query.filter_by(id=sensor_db.key_id).first()
			key_type = ast.literal_eval(api_key.type)
			inc_nested = nested_keys(data["data"])
			db_nested = nested_keys(ast.literal_eval(sensor_db.desc))
			if inc_nested == db_nested:
				if sensor_db.key_id == api_key.id and hashlib.sha256(str(data["time_stamp"] + api_key.key).encode()).hexdigest() == data["verification"]:
					new_log = APILog(sensor_id=sensor_id, dictionary=str(json.dumps(data["data"])))
					db.session.add(new_log)
					sensor_db.desc = str(json.dumps(data["data"]))
					db.session.commit()
					print("api_success")
					return Response('Update successful.', 200)
				else:
					abort(401)
			else:
				print(inc_nested)
				print(db_nested)
				abort(400)
		else:
			print(keys)
			abort(400)
	else:
		abort(405)


def make_api_backup():
	new_backup = APIBackup(date=get_date_time(), backup=api)

	db.session.add(new_backup)
	db.session.commit()

