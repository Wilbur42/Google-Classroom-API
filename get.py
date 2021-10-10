from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests_oauthlib
import requests
import json
import os
import datetime

# If modifying these scopes, delete the file token.json.
google_scopes = 'https://www.googleapis.com/auth/classroom.courses.readonly https://www.googleapis.com/auth/classroom.coursework.me.readonly'

def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./creds/token.json'):
        creds = Credentials.from_authorized_user_file('./creds/token.json', scopes=google_scopes.split(' '))
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
            flow = InstalledAppFlow.from_client_secrets_file(
                './creds/credentials.json', scopes=google_scopes.split(' '))
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./creds/token.json', 'w') as f:
            f.write(creds.to_json())
    return creds

def get_courses(course_type='id'):
    service = build('classroom', 'v1', credentials=get_creds())
    results = service.courses().list(courseStates='ACTIVE').execute()
    courses = results.get('courses', [])
    if not courses:
        print('No courses found.')
    else:
        temp = {}
        count=0
        for course in courses:
            count+=1
            if (course['courseState'] == 'ARCHIVED') or (course['name'] == '9X Computer Science  AWP'):
                courses.remove(course)
            else:
                if course_type == 'link':
                    temp[course['name']] = course['alternateLink']
                else:
                    temp[course['name']] = course['id']
    return temp

def get_classwork(courseid):
    due_coursework = []
    
    try:
        service = build('classroom', 'v1', credentials=get_creds())
    except:
        os.remove('./creds/token.json')
        service = build('classroom', 'v1', credentials=get_creds())
    result = service.courses().courseWork().list(courseId=courseid, pageSize=10).execute() 
    work = result.get('courseWork', [])
    print('len(work): ', len(work))
    for count in range(len(work)):
        print(count)
        try:
            dif = str(datetime.date(work[count]['dueDate']['year'], work[count]['dueDate']['month'], work[count]['dueDate']['day']) - datetime.date.today())
            num = int(dif.split(' day')[0])
        except:
            pass #num=0
        if num >= 0:
            due_coursework.append(work[count])
        else:
            pass
    return due_coursework

def json_print():
    file_names = ['./creds/token.json', './creds/credentials.json', 'data.json']

    for name in file_names:
        try:
            with open(name, 'r') as f:
                temp = json.load(f)
            with open(name, 'w') as f:
                f.write(json.dumps(temp, indent=4, sort_keys=True))
        except:
            pass

    print('Done!')

get_classwork()