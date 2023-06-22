import json

import googleapiclient.errors

from quickstart import get_calendar_service, HttpError

# day - 2015-05-28 format
# start_time - our and minute in 24-hour format

def get_events_raw(day):
    service = get_calendar_service()
    try:
        events_result = service.events().list(calendarId='primary', timeMin=day + 'T00:00:00+02:00',
                                              timeMax=day + 'T23:59:59+02:00',
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    except HttpError as error:
        print('An error occurred: %s' % error)

def process_events(events):
    event_list = []
    for event in events:
        event_list.append({
            'name': event['summary'],
            'day': event['start']['dateTime'][:10],
            'start': event['start']['dateTime'].split('T')[1][:5],
            'end': event['end']['dateTime'].split('T')[1][:5],
            'description': event['description'] if 'description' in event else '',
            'id': event['id']
        })
    return event_list

def get_events(day):
    events = get_events_raw(day)
    return process_events(events)

def get_event_by_id(event_id, day):
    events = get_events(day)
    for event in events:
        if event['id'] == event_id:
            return event
    return None
def create_event(event_name, day, start_time, end_time, description=''):
    service = get_calendar_service()
    try:
        event = {
            'summary': event_name,
            'description': description,
            'start': {
                'dateTime': day + 'T' + start_time + ':00+02:00',
            },
            'end': {
                'dateTime': day + 'T' + end_time + ':00+02:00',
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print('An error occurred: %s' % error)


def edit_event(event_id, new_event_name, new_day, new_start_time, new_end_time, new_description):
    service = get_calendar_service()
    try:
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        event['summary'] = new_event_name if new_event_name else event['summary']
        event['description'] = new_description if new_description else event['description']
        event['start']['dateTime'] = new_day + 'T' + new_start_time + ':00+02:00'\
            if new_day else event['start']['dateTime']
        event['end']['dateTime'] = new_day + 'T' + new_end_time + ':00+02:00' if new_day else event['end']['dateTime']
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        print('Event updated: %s' % (updated_event.get('htmlLink')))
    except googleapiclient.errors.HttpError as error:
        print('An error occurred: %s' % error)


def delete_event(event_id):
    service = get_calendar_service()
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print('Event deleted')
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    print(get_events('2023-06-22'))
    # create_event('test', '2023-06-22', '12:00', '13:00', 'test')
    edit_event('62ubvck5ve3cvtfulk4dfjrn8k', 'test2', '2023-06-22', '12:00', '13:00', 'how')
