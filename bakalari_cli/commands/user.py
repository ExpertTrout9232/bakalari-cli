import requests
from .. import auth
from ..auth import try_auth

def user_info():
    if not auth.access_token:
        return "You are not authenticated! Please login first."
    
    try:
        try_auth()
    except:
        return "Authentication failed. Please log in again."
    
    url = "https://" + auth.school_server + "/api/3/user"
    head = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {auth.access_token}"}

    response = requests.get(url, headers=head)

    output = f"""
User UID:  {response.json()["UserUID"]}
Class: {response.json()["Class"]["Abbrev"]}
Full name: {response.json()["FullName"]}
School name: {response.json()["SchoolOrganizationName"]}
User type: {response.json()["UserTypeText"]} 
Study year: {response.json()["StudyYear"]}
"""

    return output