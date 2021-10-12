from __future__ import print_function
import httplib2
import os
 
# from apiclient import discovery
# Commented above import statement and replaced it below because of
# reader Vishnukumar's comment
# Src: https://stackoverflow.com/a/30811628
 
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
 
import datetime
 
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
 
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Filter Lich Hoc'

CALENDAR_NUM = "L2"
CALENDAR_NAME = "Lịch Học Năm Nhất -test"
ENG_CLASS = "[B1.01]"
SCI_CLASS = ["L2", "L2.3", "L2.3.1"]
EXAM = "exam"
 
 
def get_credentials():
    """Lay credentials trong may
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')
 
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
 


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    def add_event(event, have_location):
        test_json = {'reminders': {'useDefault': True}}
        test_json['summary'] = event['summary']
        test_json['start'] = event['start']
        test_json['end'] = event['end']
        if have_location == True:
            test_json['location'] = event['location']
        event = service.events().insert(calendarId=calendar_ids[2], body=test_json).execute()
        print ('Event added: %s' % (test_json['summary']))

    def add_calendar(name):
        calendar = {
            'summary': name,
            'timeZone': 'Asia/Ho_Chi_Minh'
        }

        created_calendar = service.calendars().insert(body=calendar).execute()
        print("Created Calendar \"" + name + "\" " + "with id " + created_calendar['id']) 
        return created_calendar['id']
    

    calendar_ids = ['c_gj0263fted8l7qfm15shi2069c@group.calendar.google.com', 'v0qbbfube10coopf5vfiovf5qo@group.calendar.google.com']

    new_callendar_id = add_calendar(CALENDAR_NAME)
    calendar_ids.append(new_callendar_id)

    #Lay event tu lich chung cua truong
    start_date = '2021-10-01T08:00:00Z'
    end_date = '2022-01-30T23:59:00Z'
 
    if CALENDAR_NUM == "L1":
        eventsResult = service.events().list(
            calendarId=calendar_ids[1],
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            maxResults=2400,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
    if CALENDAR_NUM == "L2":
        eventsResult = service.events().list(
            calendarId=calendar_ids[0],
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            maxResults=2400,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')

    #Them event vao lich moi    
    for event in events:
        have_location = False
        if event.get('location'):
            have_location = True
        if ENG_CLASS in event['summary'] or EXAM in event['summary']:
            add_event(event, have_location)
        else:
            title = event['summary']
            class_name = title.split(' ')[0]
            if class_name in SCI_CLASS:
                add_event(event, have_location)


if __name__ == '__main__':
    main()