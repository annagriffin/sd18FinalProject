from flask import Flask, render_template, request, g
import sqlite3

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

DATABASE = '/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#------------------------------------------------------------------------
app = Flask(__name__)

all_activities = []

@app.route('/')
def maindisplay():
    #cur = get_db()
    return render_template('front_page.html', activities=all_activities)

@app.route('/inputmenu')
def get_input():
    return render_template('questions.html')

@app.route('/', methods = ['POST', 'GET'])
def show_progress_bar():


    if request.method == 'POST':
        result = request.form
        for key, value in result.items():
            if key == 'activity':
                activity=value
            if key == 'time':
                time=value

        time = int(time)

        pair = (activity,time)
        package = [pair, 0]
        all_activities.append(package)

    return render_template('front_page.html', activities=all_activities)



if __name__ == '__main__':

    app.run()
