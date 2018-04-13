# tutorial from  https://pythonspot.com/login-authentication-with-flask/
# this file was mainly written with guidence from a login authentication tutorial.
# We just wanted to experiment with the user and password database and authentication
# process. This was mainly written and used to get a better understanding of logins in Flask
# and work with databases.

from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from tabledef import *

engine = create_engine('sqlite:///tutorial.db', echo=True)
app = Flask(__name__)



@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello you have logged in successfully!"

@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
