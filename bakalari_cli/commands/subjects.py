import requests
from ..auth import try_auth, access_token, school_server

def subjects():
    if not access_token:
        return "You are not authenticated! Please login first."
    
    try:
        try_auth()
    except:
        return "Authentication failed. Please log in again."
    
    url = "https://" + school_server + "/api/3/subjects"
    head = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=head)

    output = "\nSubjects:\n"
    for i in response.json()["Subjects"]:
        output += f"""{i["SubjectAbbrev"]} - {i["SubjectName"]} ({i["TeacherAbbrev"]} - {i["TeacherName"]}: {i["TeacherEmail"]})\n"""
    
    return output