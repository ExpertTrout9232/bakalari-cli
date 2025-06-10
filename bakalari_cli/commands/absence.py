import requests
from datetime import datetime
import calendar
from .. import auth
from ..auth import try_auth

def absence():
    if not auth.access_token:
        return "You are not authenticated! Please login first."
    
    try:
        try_auth()
    except:
        return "Authentication failed. Please log in again."
    
    url = "https://" + auth.school_server + "/api/3/absence/student"
    head = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {auth.access_token}"}
    
    response = requests.get(url, headers=head)
    
    output = f"""\nAbsence percentage: {int(response.json()["PercentageThreshold"]) * 100} %\n"""
    if input("Do you want to see absence of subjects? (y/n): ").lower() == "y":
        for i in response.json()["AbsencesPerSubject"]:
            output += f"""{i["SubjectName"]}:\n"""
            output += f"""- Total lessons: {i["LessonsCount"]}\n"""
            output += f"""- General absence: {i["Base"]}\n"""
            output += f"""- Late arrivals: {i["Late"]}\n"""
            output += f"""- Early dismissals: {i["Soon"]}\n"""
            output += f"""- School events: {i["School"]}\n"""
    else:
        absences = {}

        for i in response.json()["Absences"]:
            month = calendar.month_name[datetime.fromisoformat(i["Date"]).month]
            if month not in absences:
                absences[month] = []
            
            absences[month].append(i)
        
        for month in absences:
            output += f"\n{month}:\n"
            for absence in absences[month]:
                output += f"""- {datetime.fromisoformat(absence["Date"]).strftime("%m/%d/%Y")}:\n"""
                output += f"""-- Unsolved: {absence["Unsolved"]}\n"""
                output += f"""-- Excused: {absence["Ok"]}\n"""
                output += f"""-- Missed lessons: {absence["Missed"]}\n"""
                output += f"""-- Late arrivals: {absence["Late"]}\n"""
                output += f"""-- Early dismissals: {absence["Soon"]}\n"""
                output += f"""-- School events: {absence["School"]}\n"""

    return output