# https://www.youtube.com/watch?v=8aTnmsDMldY

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.config["SECRET_KEY"] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/SoftDesFinal/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#########################################################
def create_connection(db_file):
    """create a database connection to an SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

database = "activities.db"

#Creates the table if id didn't already exist
sql_create_users_table = """ CREATE TABLE IF NOT EXISTS Users (
                                    name text NOT NULL,
                                    username text NOT NULL,
                                    password text
                                    CONSTRAINT login_unique UNIQUE (username, password)
                                    ); """
sql_create_activities_table = """ CREATE TABLE IF NOT EXISTS Activities (
                                    activity text NOT NULL,
                                    time_goal integer NOT NULL,
                                    time_done integer NOT NULL,
                                    user_id integer NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES Users (username)
                                    CONSTRAINT activity_unique UNIQUE (activity, user_id)
                                ); """
#creates the connection
conn = create_connection(database)

if conn is not None:

    # create the activities table
    create_table(conn, sql_create_users_table)
    print('Users Table Created')
    create_table(conn, sql_create_activities_table)
    print('Activities Table Created')
else:
    print("Error! cannot create the database connection.")


###########################################################
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField("password", validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField("remember me")

class RegisterForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), Email(message="Indalid Email"), Length(max=50)])
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField("password", validators=[InputRequired(), Length(min=4, max=80)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created</h1>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__=="__main__":
    app.run()
