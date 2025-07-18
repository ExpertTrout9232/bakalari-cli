import requests
import urllib.parse
import json
import os
from . import cli

TOKENS_PATH = os.path.join(os.path.dirname(__file__), "tokens.json")

school_server = ""
access_token = ""
refresh_token = ""
preserve_login = False

def login(server, username, password):
    global school_server, access_token, refresh_token, preserve_login

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

        if input("Do you want to stay logged in? (y/n): ").lower() == "y":
            preserve_login = True

            tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "school_server": school_server,
                "username": cli.user
            }

            with open(TOKENS_PATH, "w") as f:
                json.dump(tokens, f)

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

        if preserve_login == True:
            tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "school_server": school_server,
                "username": cli.user
            }

            with open(TOKENS_PATH, "w") as f:
                json.dump(tokens, f)
    else:
        raise Exception("Failed to refresh authentication tokens.")

def try_auth():
    head = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {access_token}"}
    url = "https://" + school_server + "/api/3/user"
    
    response = requests.get(url, headers=head)

    if response.status_code != 200:
        refresh_login()

def logout():
    global access_token, refresh_token, school_server, preserve_login

    preserve_login = False

    access_token = ""
    refresh_token = ""
    school_server = ""

    cli.user = "Not-Authenticated"

    try:
        with open(TOKENS_PATH, "w") as f:
            json.dump({}, f)
    except:
        pass

    return "Successfully logged out."

def login_from_file():
    global access_token, refresh_token, school_server, preserve_login

    try:
        with open(TOKENS_PATH, "r") as f:
            tokens = json.load(f)
            access_token = tokens.get("access_token", "")
            refresh_token = tokens.get("refresh_token", "")
            school_server = tokens.get("school_server", "")
            cli.user = tokens.get("username", "")
        
        if not all([access_token, refresh_token, school_server, cli.user]):
            cli.user = "Not-Authenticated"
            return False

        try: 
            try_auth()
        except:
            return False
        
        preserve_login = True
        return True
    except:
        return False