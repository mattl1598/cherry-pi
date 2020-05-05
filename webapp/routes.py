from webapp import app, db, nav
from flask import render_template, url_for, request, redirect, session
from flask_login import login_user, logout_user, current_user, AnonymousUserMixin, login_required
from webapp.models import User, Post
from webapp.forms import RegistrationForm, LoginForm
import datetime

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
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			return redirect(url_for('home'))
	return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return render_template('logged_out.html', title='Logged Out')


@app.route("/user")
@login_required
def user():
	return render_template('user.html', title='User Settings')


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST':
		user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('registered'))
	return render_template('register.html', title='Register', form=form)


@app.route("/registered")
def registered():
	return render_template('registered.html', title='Successfully Registered')