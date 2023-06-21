from flask import Flask, render_template, request, redirect
from calendar_functions import get_events, create_event, edit_event, delete_event
from datetime import date

app = Flask(__name__)

@app.route('/')
def home():
    events = get_events(date.today().isoformat())
    return render_template('index.html', events=events)

@app.route('/create', methods=['POST'])
def create():
    event_name = request.form['event_name']
    day = request.form['day']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    create_event(event_name, day, start_time, end_time, description)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
