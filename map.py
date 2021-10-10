import get
import json

course_alias = {
    "11 Add Maths (21-22) & 10 Add Maths (20-21)": "Additional Maths",
    "11 Computer Science": "Computer Science",
    "11 S1 Chemistry (GTR)": "Chemistry",
    "11-1 English PA": "English",
    "11B Geography DA": "Geography",
    "11C Design Technology MU": "Design Technology",
    "11X Biology": "Biology",
    "11X Physics AWY": "Physics",
    "Careers All Year 11": "Careers Info",
    "Coding Club": "Coding Club",
    "DOK Academic Scholars": "Academic Sholars",
    "Kestrel": "Kestrel",
    "Maths 11_1": "Maths",
    "Y11 DofE AWY": "DofE",
    "Year 11 GCSE Music NR": "Music",
    "Year 11 PE": "PE"
}


def get_alias():
    courses = get.get_courses()
    data = {}
    for course in courses:
        if course not in course_alias:
            continue
        data[course_alias[course]] = courses[course]
    return data

def update_links():
    data = get_alias()
    with open('data.json', 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

update_links()