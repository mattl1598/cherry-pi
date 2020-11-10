#!/var/www/cherry-pi-prod/venv
import sys
from webapp import app, db, nav, env_vars
from flask import render_template, url_for, request, redirect, session, jsonify, abort, Response, send_file
from flask_login import login_user, logout_user, current_user, AnonymousUserMixin, login_required
from webapp.models import User, Post, Sensor, Key, APILog, APIBackup, get_date_time, SPCode, SPPost
from webapp.forms import RegistrationForm, LoginForm, SPUploadForm
from webapp.scripts import key_64, nested_keys, one_line_graph, multi_line_graph
from webapp.upload import get_creds, upload_file
import datetime
import base64
import hashlib
import ast
import json
import requests
import markdown2

api = {"test": {"name": "test", "number": 420}}


def parse_date_time(string1):
	return datetime.datetime.strptime(string1, "%Y-%m-%d %H:%M:%S")


def get_time_stamp():
	return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


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


@app.route("/js/<filename>", methods=['GET'])
def js_loader(filename):
	if filename == "litter_listens.js":
		return send_file('/var/www/cherry-pi-prod/webapp/static/js/litter_listens.js')
	elif filename == "sp_blog.js":
		return send_file('/var/www/cherry-pi-prod/webapp/static/js/sp_blog.js')
	else:
		abort(404)

@app.route("/listens/<filename>", methods=['GET'])
def listens(filename):
	if filename == "litterpicker" or filename == "litterpicker.mp3":
		sensor_id = "Ld5zbQgU-vcqM-rV"
		data = ast.literal_eval(Sensor.query.filter_by(id=sensor_id).first().desc)
		no_of_listens = int(data["values"]["Litter Picker"]["value"])
		return {"listens": no_of_listens}
	else:
		abort(404)

@app.route("/sound/<filename>", methods=['GET'])
def sound(filename):
	if filename == "litterpicker" or filename == "litterpicker.mp3":
		sensor_id = "Ld5zbQgU-vcqM-rV"
		time_stamp = str(get_time_stamp())
		api_key = "t6DLYRPnaevdbq1vVL_jkkT0XOMMFAR1XRLDeeDF-8rApzV-KZXAdtXX5dNObOLI"
		data = ast.literal_eval(Sensor.query.filter_by(id=sensor_id).first().desc)
		header = {"content-type": "application/json"}

		data["values"]["Litter Picker"]["value"] += 1

		request_json = {
			"sensor_id": sensor_id,
			"time_stamp": str(time_stamp),
			"verification": hashlib.sha256(str(time_stamp + api_key).encode()).hexdigest(),
			"data": data
		}

		r = requests.put('http://larby.co.uk/sensor-api/update/', data=json.dumps(request_json), headers=header)

		return send_file('/var/www/cherry-pi-prod/webapp/static/audio/litterpicker.mp3')
	else:
		abort(404)


@app.route("/about")
def about():
	return render_template('about.html', title="About")

@app.route("/sp-post")
def sp_post():
	post_id = request.args.get('post', default=0, type=int)
	request_src = request.args.get('src', default="", type=str)
	print(post_id)
	if post_id:
		valid_ids_db = SPPost.query.with_entities(SPPost.id).all()
		valid_ids = []
		for tup in valid_ids_db:
			valid_ids.append(tup[0])
		print(valid_ids)
		if post_id in valid_ids:
			post = SPPost.query.filter_by(id=post_id).first()
			print(post)
			html_content = markdown2.markdown(post.content)
			if request_src == "js":
				return render_template("sppost_js.html", post=post, content=html_content)
			else:
				return render_template('sppost.html', post=post)
		else:
			abort(404)


@app.route("/sp/upload", methods=["GET", "POST"])
def upload():
	error = ""
	link_code = request.args.get('code', default="", type=str)
	form = SPUploadForm()
	# codes = ["SP_TEST", "SP_TEST2"]
	link_code = request.args.get('code', default="", type=str)
	codes_db = SPCode.query.filter_by(active="True").with_entities(SPCode.id).all()
	codes = []
	for tup in codes_db:
		codes.append(tup[0])
	if request.method == 'POST':
		code = form.upload_code.data
		print(code)
		print(codes)
		code_db = SPCode.query.filter_by(id=code).first()
		if code in codes:
			print("valid code")
			filename = form.file.data.filename
			mime = form.file.data.mimetype
			file = request.files["file"].read()
			file_data = {"file_name": str(code_db.char) + " " + str(code) + filename[filename.rfind("."):], "mimetype": mime}
			upload_file(file, file_data, get_creds())
			code_db.active = "False"
			db.session.commit()
			return redirect(url_for("success"))
		else:
			error = "Invalid Upload Code"
	return render_template("upload.html", title="Upload", form=form, error=error, link_code=link_code)


@app.route("/sp/upload/success", methods=["GET"])
def success():
	return render_template("success.html", title="Success")


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


@app.route("/graph/<sensor_id>", methods=['GET'])
def graph(sensor_id):
	if (request.method == 'GET') and (Sensor.query.filter_by(id=sensor_id).first() is not None):
		sensor_log = APILog.query.filter_by(sensor_id=sensor_id).all()
		graph_series = ast.literal_eval(sensor_log[0].dictionary)["values"].keys()
		graph_tuples = [(str(get_date_time()), ast.literal_eval(Sensor.query.filter_by(id=sensor_id).first().desc),)]
		# graph_tuples = []
		last_dict = None
		for item in sensor_log:
			# if last_dict is not None:
			# 	just_before = str((datetime.datetime.strptime(str(item.date), "%Y-%m-%d %H:%M:%S") - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S"))
			# 	graph_tuples.append((just_before, ast.literal_eval(last_dict)))
			graph_tuples.append((str(item.date), ast.literal_eval(item.dictionary),))
			# last_dict = str(item.dictionary)
		graph_tuples.sort(key=lambda tup: tup[0])
		data = graph_tuples
		if len(list(graph_series)) == 1:
			image = str(one_line_graph(graph_tuples, list(graph_series)))[2:-1]
		else:
			image = str(multi_line_graph(graph_tuples, list(graph_series)))[2:-1]
		
		return render_template('graph.html', title="Graph of " + str(sensor_id), data=data, image=image)
	else:
		abort(404)

@app.route("/graph/<sensor_id>/last", methods=['GET'])
def graph_range(sensor_id):
	if (request.method == 'GET') and (Sensor.query.filter_by(id=sensor_id).first() is not None):

		days = request.args.get('days', default=0, type=int)
		hours = request.args.get('hours', default=0, type=int)
		minutes = request.args.get('minutes', default=0, type=int)
		if not (days or hours or minutes):
			days = 30
		target_date = datetime.datetime.today() - datetime.timedelta(days=days, hours=hours, minutes=minutes)
		xlim = [target_date, datetime.datetime.today()]
		print(target_date)
		sensor_log = APILog.query.filter_by(sensor_id=sensor_id).all()
		graph_series = ast.literal_eval(sensor_log[0].dictionary)["values"].keys()
		graph_tuples = []
		for item in sensor_log:
			if item.date > target_date:
				new_tuple = (str(item.date), ast.literal_eval(item.dictionary),)
				graph_tuples.append(new_tuple)
		data = graph_series
		print(len(list(graph_series)))
		if len(graph_tuples) != 0:
			if len(list(graph_series)) == 1:
				image = str(one_line_graph(graph_tuples, list(graph_series)))[2:-1]
			else:
				image = str(multi_line_graph(graph_tuples, list(graph_series)))[2:-1]
		else:
			abort(404)
		return render_template('graph.html', title="Graph of " + str(sensor_id), data=data, image=image)
	else:
		abort(404)


@app.route("/sensor-api/get/<sensor_id>", methods=['GET'])
def sensor_api(sensor_id):
	if (request.method == 'GET') and (Sensor.query.filter_by(id=sensor_id).first() is not None):
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

