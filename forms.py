
"""This file contains all of the flakforms that are used in this program"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    """ This class uses FlaskForm and creates a form on the login page. There are
    entries for the username and password."""

    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField("Remember me")


class RegisterForm(FlaskForm):
    """ This class uses FlaskForm and creates a form for new users to make an account. An email,
    username, and password are required. """

    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid Email"), Length(max=50)])
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=80)])


class ActivitiesForm(FlaskForm):
    """ This class uses FlaskForm and creates a form for users to add new activites. It takes an activity name
    goal time, both chosen by the user. """

    activity_name = StringField("Activity", validators=[InputRequired(), Length(min=1, max=100)])
    goal_time = IntegerField("Time", validators=[InputRequired()])
