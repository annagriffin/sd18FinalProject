
# https://www.youtube.com/watch?v=8aTnmsDMldY

from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config["SECRET_KEY"] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/anna/FinalProject/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class Activity(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text)
    activity_name = db.Column(db.String(15))
    goal_time = db.Column(db.Integer)
    progress = db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField("Remember me")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=80)])

class ActivitiesForm(FlaskForm):
    activity_name = StringField("Activity", validators=[InputRequired(), Length(min=1, max=100)])
    goal_time = IntegerField("Time", validators=[InputRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'

    return render_template('index.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    i = 0
    complete_list = []
    while i < len(activity):
        temp_list = []
        temp_list.append(activity[i].activity_name.capitalize())
        temp_list.append(activity[i].goal_time)
        temp_list.append(activity[i].progress)
        color_determiner = i % 4
        if color_determiner == 0:
            color_determiner = 'success'
        if color_determiner == 1:
            color_determiner = 'info'
        if color_determiner == 2:
            color_determiner = 'warning'
        if color_determiner == 3:
            color_determiner = 'danger'
        temp_list.append(color_determiner)
        complete_list.append(temp_list)
        i += 1


    # if request.method == 'POST':
    #     tag = int(request.form['tag'])
    #     activity[tag].progress += 1
    #     db.session.commit()
    #     return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=users_name, complete_list=complete_list) # activity_list=activity_list, time_goal_list=time_goal_list, current_progress_list=current_progress_list)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    i = 0
    complete_list = []
    while i < len(activity):
        temp_list = []
        temp_list.append(activity[i].activity_name.capitalize())
        temp_list.append(activity[i].goal_time)
        temp_list.append(activity[i].progress)
        color_determiner = i % 4
        if color_determiner == 0:
            color_determiner = 'success'
        if color_determiner == 1:
            color_determiner = 'info'
        if color_determiner == 2:
            color_determiner = 'warning'
        if color_determiner == 3:
            color_determiner = 'danger'
        temp_list.append(color_determiner)
        complete_list.append(temp_list)
        i += 1

    if request.method == 'POST':
        tag = int(request.form['tag_a'])
        activity[tag].progress += 1
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=users_name, complete_list=complete_list)

@app.route('/subtract', methods=['GET', 'POST'])
@login_required
def subtract():
    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    i = 0
    complete_list = []
    while i < len(activity):
        temp_list = []
        temp_list.append(activity[i].activity_name.capitalize())
        temp_list.append(activity[i].goal_time)
        temp_list.append(activity[i].progress)
        color_determiner = i % 4
        if color_determiner == 0:
            color_determiner = 'success'
        if color_determiner == 1:
            color_determiner = 'info'
        if color_determiner == 2:
            color_determiner = 'warning'
        if color_determiner == 3:
            color_determiner = 'danger'
        temp_list.append(color_determiner)
        complete_list.append(temp_list)
        i += 1

    if request.method == 'POST':
        tag = int(request.form['tag_s'])
        activity[tag].progress -= 1
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=users_name, complete_list=complete_list)

@app.route('/clear', methods=['GET', 'POST'])
@login_required
def clear():
    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    i = 0
    complete_list = []
    while i < len(activity):
        temp_list = []
        temp_list.append(activity[i].activity_name.capitalize())
        temp_list.append(activity[i].goal_time)
        temp_list.append(activity[i].progress)
        color_determiner = i % 4
        if color_determiner == 0:
            color_determiner = 'success'
        if color_determiner == 1:
            color_determiner = 'info'
        if color_determiner == 2:
            color_determiner = 'warning'
        if color_determiner == 3:
            color_determiner = 'danger'
        temp_list.append(color_determiner)
        complete_list.append(temp_list)
        i += 1

    if request.method == 'POST':
        tag = int(request.form['tag_c'])
        activity[tag].progress = 0
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=users_name, complete_list=complete_list)


@app.route('/add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = ActivitiesForm()
    if form.validate_on_submit():
        new_activity = Activity(user_id=str(current_user), activity_name=form.activity_name.data, goal_time=form.goal_time.data, progress=0)
        db.session.add(new_activity)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('activitiesform.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__=="__main__":
    app.run()
