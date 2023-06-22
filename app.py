from flask import Flask, render_template, request, redirect
from calendar_functions import get_events, create_event, edit_event, delete_event, get_event_by_id

app = Flask(__name__)

@app.route('/')
def home():
    events = get_events()
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

@app.route('/edit/<event_id>', methods=['POST'])  # decorator
def edit(event_id):
    event_name = request.form['event_name']
    day = request.form['day']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    edit_event(event_id, event_name, day, start_time, end_time, description)
    return redirect('/')

@app.route('/edit/<event_id>')
def show_edit_page(event_id):
    event = get_event_by_id(event_id)
    return render_template('edit.html', event=event, event_id=event_id)

@app.route('/delete/<event_id>')
def delete(event_id):
    delete_event(event_id)
    return redirect('/')


# flask run --port 8000
if __name__ == '__main__':
    app.run(port=8000, debug=True)
