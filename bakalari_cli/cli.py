import sys
import os
from getpass import getpass
from .auth import login, login_from_file, logout
from .commands.user import user_info
from .commands.subjects import subjects
from .commands.absence import absence
from .commands.marks import marks

commands = ["login", "logout", "user", "subjects", "absence", "marks", "exit", "clear", "help"]
user = "Not-Authenticated"

if sys.platform == "win32":
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import WordCompleter

    completer = WordCompleter(commands, ignore_case=True)
else:
    import readline 

def request_input(prompt_text):
    if sys.platform == "win32":
        return prompt(prompt_text, completer=completer)
    else:
        def completer_readline(text, state):
            options = [cmd for cmd in commands if cmd.startswith(text.lower())]

            if state < len(options):
                return options[state]
            else:
                return None

        readline.set_completer(completer_readline)
        readline.parse_and_bind("tab: complete")

        return input(prompt_text)

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
        action = request_input(f"[Bakalari-CLI][{user}]> ").lower().strip()
        
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
        elif action == "marks":
            print(marks())
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
MARKS - Displays user's marks
CLEAR - Clears the screen
HELP - Shows this help
EXIT - Exits Bakalari-CLI
"""

    return output