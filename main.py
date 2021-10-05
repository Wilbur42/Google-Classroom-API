from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests_oauthlib
import requests
import json

# If modifying these scopes, delete the file token.json.
google_scopes = 'https://www.googleapis.com/auth/classroom.courses.readonly https://www.googleapis.com/auth/classroom.coursework.me.readonly'

def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes=google_scopes.split(' '))
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=google_scopes.split(' '))
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    return creds

def get_links():
    service = build('classroom', 'v1', credentials=get_creds())
    # Call the Classroom API
    results = service.courses().list(pageSize=20).execute()
    courses = results.get('courses', [])
    #print(courses)

    if not courses:
        print('No courses found.')
    else:
        temp = {}
        for course in courses:
            if (course['courseState'] == 'ARCHIVED'):
                courses.remove(course)
            else:
                temp[course['name']] = course['alternateLink']
    return temp

def get_id():
    service = build('classroom', 'v1', credentials=get_creds())
    # Call the Classroom API
    results = service.courses().list(pageSize=20).execute()
    courses = results.get('courses', [])
    #print(courses)

    if not courses:
        print('No courses found.')
    else:
        temp = {}
        for course in courses:
            if (course['courseState'] == 'ARCHIVED'):
                courses.remove(course)
            else:
                temp[course['name']] = course['id']
    return temp

def get_classwork():
    courseId = '11C Design Technology MU'
    id = 158203244700

    service = build('classroom', 'v1', credentials=get_creds())
    #print(service.courses().courseWork().list(courseId=courseId))
    #results = service.courses().courseWork().list(courseId=courseId).execute()
    #work = results.get('courseWork', [])
    print(f'https://classroom.googleapis.com/v1/courses/{courseId}/courseWork')
    work = requests.get(f'https://classroom.googleapis.com/v1/courses/{courseId}/courseWork')
    print(work)

def json_print():
    file_names = ['token', 'credentials', 'data']

    for name in file_names:
        try:
            with open(name+'.json', 'r') as f:
                temp = json.load(f)
            with open(name+'.json', 'w') as f:
                f.write(json.dumps(temp, indent=4, sort_keys=True))
        except:
            pass

    print('Done!')

if __name__ == '__main__':
    get_creds()
    #print(get_id())
    #get_classwork()