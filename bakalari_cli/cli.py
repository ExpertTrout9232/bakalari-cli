import sys
import os
from getpass import getpass
from .auth import login, login_from_file, logout
from .commands.user import user_info
from .commands.subjects import subjects
from .commands.absence import absence

if sys.platform == "win32":
    import pyreadline as readline
else:
    import readline 

user = "Not-Authenticated"

commands = ["login", "logout", "user", "subjects", "absence", "exit", "clear", "help"]

def completer(text, state):
    options = [cmd for cmd in commands if cmd.startswith(text.lower())]

    if state < len(options):
        return options[state]
    else:
        return None
    
readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def main():
    global user

    if login_from_file():
        print(f"Logged in as {user}")
    elif len(sys.argv) > 1 and len(sys.argv) != 4:
        raise ValueError("Usage: python -m bakalari_cli <server> <username> <password>")
    elif len(sys.argv) == 4:
        print(login(sys.argv[1], sys.argv[2], sys.argv[3]))
    
    print("Welcome to Bakalari-CLI!")

    while True:
        action = input(f"[Bakalari-CLI][{user}]> ").lower()
        
        if not action:
            continue

        if action == "login":
            print(login(input("Server: "), input("Username: "), getpass("Password: ")))
        elif action == "logout":
            print(logout())
        elif action == "user":
            print(user_info())
        elif action == "subjects":
            print(subjects())
        elif action == "absence":
            print(absence())
        elif action == "exit":
            print("See you later!")
            return
        elif action == "clear":
            if sys.platform == "win32":
                os.system("cls")
            else:
                os.system("clear")
        elif action == "help":
            print(help())
        else:
            print("Invalid command! Use \"Help\" for help.")

def help():
    output = """
Bakalari-CLI Commands:
LOGIN - Authenticates to the school server with credentials
LOGOUT - Log out of the app
USER - Shows info about the authenticated user
SUBJECTS - Displays a list of user's subjects with teachers
ABSENCE - Displays user's absence records
CLEAR - Clears the screen
HELP - Shows this help
EXIT - Exits Bakalari-CLI
"""

    return output