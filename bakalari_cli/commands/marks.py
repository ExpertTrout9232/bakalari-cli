import requests
from datetime import datetime
from .. import auth
from ..auth import try_auth

def marks():
    if not auth.access_token:
        return "You are not authenticated! Please login first."
    
    try:
        try_auth()
    except:
        return "Authentication failed. Please log in again."
    
    url = "https://" + auth.school_server + "/api/3/marks"
    subjects_url = "https://" + auth.school_server + "/api/3/subjects"
    head = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {auth.access_token}"}

    response = requests.get(url, headers=head)
    subjects_response = requests.get(subjects_url, headers=head)

    if input("Do you want to see marks sorted by date? (y/n): ").lower() == "y":
        output = f"""\nMarks sorted by date:\n"""
        
        marks = []
        subjects  = subjects_response.json()["Subjects"]

        for i in response.json()["Subjects"]:
            for j in i["Marks"]:
                j["SubjectName"] = i["Subject"]["Name"]
                marks.append(j)

        for i in subjects:
            for j in marks:
                if i["TeacherID"] == j["TeacherId"]:
                    j["TeacherName"] = i["TeacherName"]

        marks.sort(key=lambda x: x["MarkDate"], reverse=True)

        for i in marks:
            output += f"""{datetime.fromisoformat(i["MarkDate"]).strftime("%m/%d/%Y")} - {i["MarkText"]} (Weight: {i["Weight"]}) - {i["SubjectName"]} ({i["TeacherName"]}) - {i["Caption"]}\n"""
    else:
        output = f"""\nMarks:\n"""

        subjects = subjects_response.json()["Subjects"]
        teachers = {}

        for i in subjects:
            teachers[i["TeacherID"]] = i["TeacherName"]

        for i in response.json()["Subjects"]:
            output += f"""{i["Subject"]["Name"]} (Average: {i["AverageText"][:4]}):\n"""

            for j in i["Marks"]:
                output += f"""- {datetime.fromisoformat(j["MarkDate"]).strftime("%m/%d/%Y")} - {j["MarkText"]} (Weight: {j["Weight"]}) - {teachers.get(j["TeacherId"])} - {j["Caption"]}\n"""



    return output        