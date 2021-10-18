from __future__ import print_function
import httplib2
import os
import multiprocessing
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
 
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
 
# Muốn đổi tài khoản thì xóa thư mục này
# C:/Users/<tên_tài_khoản>/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Filter Lich Hoc'

CALENDAR_NUM = "L2"
CALENDAR_NAME = "Lịch Học Năm Nhất"
ENG_CLASS = "[B1.01]"
SCI_CLASS = ["L2", "L2.3", "L2.3.2"]
EXAM = "exam"

blacklist_field = ['kind','id','etag','status','htmlLink','created', 'updated','creator','organizer','recurringEventId','originalStartTime','iCalUID','sequence','eventType','attendees']
#calendar_ids[0] là L2, [1] là L1 
calendar_ids = ['c_gj0263fted8l7qfm15shi2069c@group.calendar.google.com', 'v0qbbfube10coopf5vfiovf5qo@group.calendar.google.com']
seclected_events = []

start_date = '2021-10-01T01:00:00Z'
end_date = '2022-01-30T23:59:00Z'
count = 0
#Lay credentials trong may
def get_credentials():
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

credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

def add_event(unparsed_event, calendarid):
    global count
    parsedEvent = parseEvent(unparsed_event)
    count += 1
    event = service.events().insert(calendarId=calendarid, body=parsedEvent).execute()
    print ("Event added: {} at {}".format(parsedEvent['summary'], parsedEvent['start']['dateTime']))

def add_calendar(name):
    calendar = {
        'summary': name,
        'timeZone': 'Asia/Ho_Chi_Minh'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    print("Created Calendar \"" + name + "\" " + "with id " + created_calendar['id']) 
    return created_calendar['id']

def parseEvent(rawEvent):
    parsedEvent = {}
    for key in rawEvent:
        if key not in blacklist_field:
            parsedEvent[key] = rawEvent[key]
    return parsedEvent


#Lay event tu lich chung cua truong
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
    if ENG_CLASS in event['summary'] or EXAM in event['summary']:
        seclected_events.append(event)
    else:
        title = event['summary']
        class_name = title.split(' ')[0]
        if class_name in SCI_CLASS:
            seclected_events.append(event)

#Multiprocessing -----------------
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def do_job(job_id, data_slice, calendarid):
    for item in data_slice:
        add_event(item,calendarid)

def dispatch_jobs(data, job_number, calendarid):
    total = len(data)
    chunk_size = int(total / job_number) + 1
    slice = list(chunks(data, chunk_size))
    jobs = []

    for i, s in enumerate(slice):
        j = multiprocessing.Process(target=do_job, args=(i, s, calendarid))
        jobs.append(j)
    for j in jobs:
        j.start()
#Multiprocessing -----------------

def main():
    pass
    

if __name__ == '__main__':
    new_calendar_id = add_calendar(CALENDAR_NAME)
    dispatch_jobs(seclected_events, 2, new_calendar_id)
    main()
