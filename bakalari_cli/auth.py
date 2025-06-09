import requests
import urllib.parse
from . import cli

school_server = ""
access_token = ""
refresh_token = ""

def login(server, username, password):
    global school_server, access_token, refresh_token

    if len(server.split('/')) > 1:
        try:
            school_server = server.split('/')[2]
        except:
            return "Invalid server!"
    else:
        school_server = server
    
    url = "https://" + school_server + "/api/login"
    body = f"client_id=ANDR&grant_type=password&username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}"
    head = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(url, data=body, headers=head)
    except:
        return "Invalid server!"
    
    if response.status_code == 200:
        cli.user = username
        access_token = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]

        return "Authentification successful."
    else:
        return "Authentification failed."
    
def refresh_login():
    global access_token, refresh_token

    url = "https://" + school_server + "/api/login"
    body = f"client_id=ANDR&grant_type=refresh_token&refresh_token={refresh_token}"
    head = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=body, headers=head)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        refresh_token = response.json()["refresh_token"]
    else:
        raise Exception("Failed to refresh authentication tokens.")

def try_auth():
    head = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {access_token}"}
    url = "https://" + school_server + "/api/3/user"
    
    response = requests.get(url, headers=head)

    if response.status_code == 401:
        refresh_login()