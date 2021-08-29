from pprint import pprint
from Google import Create_Service, convert_to_RFC_datetime

CLIENT_SECRET_FILE = 'login.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# _________________ Calendar _______________________
request_body = {'summary': 'Physics'}
"""
Create a calendar
"""
response = service.calendars().insert(body=request_body).execute()
print(response)
"""
Delete a calendar
"""
service.calendars().delete(
    calendarId='fru58fsbkvfg3cj21rbe7nlivc@group.calendar.google.com').execute(
    )
"""
List calendar
"""
response = service.calendarList().list(maxResults=250,
                                       showDeleted=False,
                                       showHidden=False).execute()
calendarItems = response.get('items')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = service.calendarList().list(maxResults=250,
                                           showDeleted=False,
                                           showHidden=False,
                                           pageToken=nextPageToken).execute()
    calendarItems.extend(response.get('items'))
    nextPageToken = response.get('nextPageToken')

pprint(calendarItems)
"""
Update
"""
myCalendar = filter(lambda x: 'Physics' in x['summary'], calendarItems)
myCalendar = next(myCalendar)

myCalendar['summary'] = 'test hì hì'
myCalendar['description'] = 'Mon vat li hoc rat kho'

service.calendars().update(calendarId=myCalendar['id'],
                           body=myCalendar).execute()
"""
Color
"""
colorProfiles = service.colors().get().execute()
pprint(colorProfiles)

# ___________________________ Events ________________________
"""
Create an event
"""
colors = service.colors().get().execute()
pprint(colors)

recurrence = ["RRULE:FREQ=WEEKLY;COUNT=2"]

hour_adjustment = -7
event_request_body = {
    'start': {
        'dateTime': convert_to_RFC_datetime(2021, 8, 30, 8 + hour_adjustment,
                                            30),
        'timeZone': 'Asia/Ho_Chi_Minh'
    },
    'end': {
        'dateTime': convert_to_RFC_datetime(2021, 8, 30, 9 + hour_adjustment,
                                            0),
        'timeZone': 'Asia/Ho_Chi_Minh'
    },
    'summary':
    'Family Lunch',
    'description':
    'Create from Vs Code',
    'colorId':
    5,
    'status':
    'confirmed',
    'transparency':
    'opaque',
    'visibility':
    'private',
    'location':
    'Binh Dinh',
    'attachment': [{
        'fileUrl':
        'https://drive.google.com/file/d/1jGuIyGv-ubjFRIYEolxa0F9zoSHYOKyD/edit',
        'title': 'Day la Attachment'
    }],
    'attendees': [{
        'displayName': 'Vuong',
        'comment': 'I enjoy coding',
        'email': 'tranduyvuong100@gmail.com',
        'optional': False,
        'organizer': True,
        'responseStatus': 'accepted'
    }],
    'recurrence':
    recurrence
}

maxAttendees = 50
sendNotification = True
sendUpdate = "all"
supportsAttachments = True

response = service.events().insert(calendarId='primary',
                                   maxAttendees=maxAttendees,
                                   sendNotifications=sendNotification,
                                   sendUpdates=sendUpdate,
                                   supportsAttachments=supportsAttachments,
                                   body=event_request_body).execute()

eventId = response['id']

pprint(response)
"""
Update an event
"""
start_datetime = convert_to_RFC_datetime(2021, 8, 30, 8 + hour_adjustment, 30),
end_datetime = convert_to_RFC_datetime(2021, 8, 30, 9 + hour_adjustment, 0),
response['start']['dateTime'] = start_datetime
response['end']['dateTime'] = end_datetime
response['summary'] = 'Vuong dep trai'
response['Description'] = 'Having Family Dinner'
service.events().update(
    calendarId='primary',
    eventId=eventId,
    body=response
).execute()

"""
Delete an event
"""
service.events().delete(calendarId='primary',eventId=eventId).execute()