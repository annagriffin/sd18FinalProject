# We used a tutorial by Printed Pretty to help us structure our FlaskLogin system
# https://www.com/watch?v=8aTnmsDMldY
""" This is the python file of the TimeTracker app. """

from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from forms import LoginForm, ActivitiesForm, RegisterForm


app = Flask(__name__)
app.config["SECRET_KEY"] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/anna/FinalProject/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'


class User(UserMixin, db.Model):
    """ This class defines a user and stores users' infromation in a table in
    a database. When a user makes an account, their username, email, and password
    get stored in the datbase. """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class Activity(db.Model):
    """ This class defines an activity object. An activity consists of a name,
    goal time, and current progress. The user_id  is also included in this object
    so that it is easily accessible when filterting activites by users."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text)
    activity_name = db.Column(db.String(15))
    goal_time = db.Column(db.Integer)
    progress = db.Column(db.Integer)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    """ A login form is created and prompts the
    user to login and provides a link for new users so that they can easily signup. """

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
    """ A registraction form is created and askes the new user to
    input a username, email, and password. Then it addes the information to the database and redirects
    the user back to the login page. """

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


def create_complete_list():
    """ Creates a list of all the activities. Each activity consits of the
    name, the goal time and the progress time. This data is retreived by
    quering the databse. There is also an additional element in the list,
    this just allows the progress bars to appear as different colors when
    the dashboard template is rendered"""
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    i = 0
    num_color = 4
    complete_list = []
    print(type(activity))
    while i < len(activity):
        temp_list = []
        temp_list.append(activity[i].activity_name.capitalize())
        temp_list.append(activity[i].goal_time)
        temp_list.append(activity[i].progress)

        # Determines the color of the progress bar. Labels are assigned on a 4
        # color cycle and are used in the html
        color_determiner = i % num_color
        if color_determiner == 0:
            color_determiner = 'danger'
        if color_determiner == 1:
            color_determiner = 'warning'
        if color_determiner == 2:
            color_determiner = 'info'
        if color_determiner == 3:
            color_determiner = 'success'
        temp_list.append(color_determiner)
        complete_list.append(temp_list)
        i += 1

    return complete_list


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """ Filtering by the current user, a list of all of
    the activites  is created. """

    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    complete_list = create_complete_list()

    return render_template('dashboard.html', user=users_name, complete_list=complete_list)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """ The main purpose of this function is to add an hour to the specified activity. The change is
    commited to the database and then the user is redirected to the dashboard so that it
    can update automitcally with the new value in the database. """

    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    complete_list = create_complete_list()

    # Adds an hour to the progress
    if request.method == 'POST':
        tag = int(request.form['tag_a'])
        activity[tag].progress += 1
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=users_name, complete_list=complete_list)


@app.route('/subtract', methods=['GET', 'POST'])
@login_required
def subtract():
    """ This route's main purpose is to subtract an hour to the specified activity. The change is
    commited to the database and then the user is redirected to the dashboard so that it
    can update automitcally with the new value in the database. """

    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    complete_list = create_complete_list()

    # Subtracts an hour from the progress
    if request.method == 'POST':
        tag = int(request.form['tag_s'])
        activity[tag].progress -= 1
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=users_name, complete_list=complete_list)


@app.route('/clear', methods=['GET', 'POST'])
@login_required
def clear():
    """ This function clears the specified activity. The change is
    commited to the database and then the user is redirected to the dashboard so that it
    can update automitcally with the new value in the database. """

    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    complete_list = create_complete_list()

    # Resets the progress to 0
    if request.method == 'POST':
        tag = int(request.form['tag_c'])
        activity[tag].progress = 0
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=users_name, complete_list=complete_list)



@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    """ This function subtracts an hour to the specified activity. The change is
    commited to the database and then the user is redirected to the dashboard so that it
    can update automitcally with the new value in the database. """

    users_name = current_user.username.capitalize()
    activity = Activity.query.filter_by(user_id=str(current_user)).all()

    complete_list = create_complete_list()

    if request.method == 'POST':
        tag = int(request.form['tag_d'])
        db.session.delete(activity[tag])
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', user=users_name, complete_list=complete_list)


@app.route('/add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    """ An activities form is created and
    commits the new activity and time to the database. """

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
    """ This fuctions logs out the current user """
    logout_user()
    return redirect(url_for('index'))



if __name__=="__main__":
    app.run()
