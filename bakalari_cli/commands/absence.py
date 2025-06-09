import requests
from ..auth import try_auth, access_token, school_server

def absence():
    if not access_token:
        return "You are not authenticated! Please login first."
    
    try:
        try_auth()
    except:
        return "Authentication failed. Please log in again."
    
    url = "https://" + school_server + "/api/3/absence/student"
    head = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=head)
    
    if input("Do you want to see absence of subjects? (y/n): ").lower() == "y":
        output = "\nAbsence:\n"
        for i in response.json()["AbsencesPerSubject"]:
            output += f"""{i["SubjectName"]}:\n"""
            output += f"""- Total lessons: {i["LessonsCount"]}\n"""
            output += f"""- General absence: {i["Base"]}\n"""
            output += f"""- Late arrivals: {i["Late"]}\n"""
            output += f"""- Early dismissals: {i["Soon"]}\n"""
            output += f"""- School events: {i["School"]}\n"""
    else:
        output = "\nAbsence:\n"

    return output