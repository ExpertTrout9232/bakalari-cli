import requests
from .. import auth
from ..auth import try_auth

def subjects():
    if not auth.access_token:
        return "You are not authenticated! Please login first."
    
    try:
        try_auth()
    except:
        return "Authentication failed. Please log in again."
    
    url = "https://" + auth.school_server + "/api/3/subjects"
    head = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {auth.access_token}"}

    response = requests.get(url, headers=head)

    output = "\nSubjects:\n"
    for i in response.json()["Subjects"]:
        output += f"""{i["SubjectAbbrev"]} - {i["SubjectName"]} ({i["TeacherAbbrev"]} - {i["TeacherName"]}: {i["TeacherEmail"]})\n"""
    
    return output