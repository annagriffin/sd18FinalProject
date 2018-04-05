from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def get_information():
    return render_template('questions.html')

@app.route('/display', methods = ['POST', 'GET'])
def show_progress_bar():

    if request.method == 'POST':
        result = request.form
        for key, value in result.items():
            if key == 'activity':
                activity=value
            if key == 'time':
                time=value
    return render_template('display.html', activity=activity, time=time)



if __name__ == '__main__':
    app.run()
