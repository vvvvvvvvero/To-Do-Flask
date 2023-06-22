from flask import Flask, render_template, request, redirect, session
from calendar_functions import get_events, create_event, edit_event, delete_event, get_event_by_id
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = 'avo11NAILariok!2002eme71'

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_day = request.args.get('selected_day')
    today = date.today().isoformat()
    error_message = session.pop('error_message', None)

    if selected_day:
        events = get_events(selected_day)
    else:
        events = get_events(today)
        selected_day = today
    return render_template('index.html', events=events, selected_day=selected_day,
                           today=today, error_message=error_message)


@app.route('/create', methods=['POST'])
def create():
    event_name = request.form['event_name']
    day = request.form['day']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    start_datetime = datetime.strptime(start_time, '%H:%M')
    end_datetime = datetime.strptime(end_time, '%H:%M')

    if start_datetime < end_datetime:
        create_event(event_name, day, start_time, end_time, description)
        return redirect('/')
    else:
        error_message = 'Start time must be earlier than end time.'
        session['error_message'] = error_message
        return redirect('/')


@app.route('/edit/<event_id>', methods=['POST'])  # decorator
def edit(event_id):
    event_name = request.form['event_name']
    day = request.form['day']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    description = request.form['description']
    start_datetime = datetime.strptime(start_time, '%H:%M')
    end_datetime = datetime.strptime(end_time, '%H:%M')

    if start_datetime < end_datetime:
        edit_event(event_id, event_name, day, start_time, end_time, description)
        return redirect('/')
    else:
        error_message = 'Start time must be earlier than end time.'
        session['error_message'] = error_message
    return redirect('/')

@app.route('/edit/<event_id>')
def show_edit_page(event_id):
    day = request.args.get('selected_day', date.today().isoformat())
    event = get_event_by_id(event_id, day)
    return render_template('edit.html', event=event, event_id=event_id)

@app.route('/delete/<event_id>')
def delete(event_id):
    delete_event(event_id)
    return redirect('/')


# flask run --port 8000
if __name__ == '__main__':
    app.run(port=8000, debug=True)


