# This file has a very brief example of what the experince of adding an activity and time will be like for the user.
# Right now the buttons are not fully functioning but the adding events and times functionaltiy is there

from flask import Flask, render_template, request
import datacollect
app = Flask(__name__)

all_activities = []

@app.route('/')
def maindisplay():
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
        print(result)
        time = int(time)
        print(type(time))
        pair = (activity,time)
        package = [pair, 0]
        all_activities.append(package)

    return render_template('front_page.html', activities=all_activities)



if __name__ == '__main__':
    app.run()
