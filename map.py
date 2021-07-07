import getlinks
import json

course_alias = {
'10 FSMQ Additional Maths (2020-21)' : 'Additional Maths',
'10B Geography DA' : 'Geography',
'Maths 10 Set 1 (2020-21)' : 'Maths',
'10 Music NR' : 'Music',
'10X Physics AWY' : 'Physics',
'10X Biology EV' : 'Biology',
'Year 10B Form Class' : 'Form Class',
'10 Computer Science' : 'Computer Science',
'10C Design Technology MU' : 'DT',
'10X Chemistry GTR' : 'Chemistry',
'10-1 English PA' : 'English',
'Chichester' : 'Chichester',
'10 DofE AWY' : 'DOFE',
}


def get_classes():
    courses = getlinks.main()
    data = {}
    for course in courses:
        if course not in course_alias:
            continue
        data[course_alias[course]] = courses[course]
    return data

def update_links():
    data = get_classes()
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))

update_links()