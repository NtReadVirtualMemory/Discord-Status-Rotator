import requests
import time
import json
import os
from keep_alive import keep_alive
from colorama import init, Fore

def read_statuses(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def text_to_list(input_string):
    return [text.strip() for text in input_string.split(",")]

def get_user_info(token):
    header ={
        'authorization': token
    }
    r = requests.get("https://discord.com/api/v10/users/@me", headers=header)
    if r.status_code == 200:
        user_info = r.json()
        return user_info["username"], True
    else:
        return "Invalid token", False

def change_status(token, message, status):
    header = {
        'authorization': token
    }

    current_status = requests.get("https://discord.com/api/v10/users/@me/settings", headers=header).json()

    custom_status = current_status.get("custom_status", {})
    if custom_status is None:
        custom_status = {}
    custom_status["text"] = message

    jsonData = {
        "custom_status": custom_status,
        "activities": current_status.get("activities", []),
        "status": status
    }

    r = requests.patch("https://discord.com/api/v10/users/@me/settings", headers=header, json=jsonData)
    return r.status_code

def color_text(text, color_code):
    return f"{color_code}{text}{Fore.RESET}"

init()  

token = os.environ.get("Token")
speed_rotator = 5
status_sequence = ["dnd"] #["online", "idle", "dnd"]

status_count = 0  

keep_alive()

while True:
    current_status = status_sequence[status_count % len(status_sequence)]
    user_info, is_valid_token = get_user_info(token)
    statuses = text_to_list(os.environ.get("Statuses")) ## Example: "Hello,hi,real,lol"

    status = statuses[status_count % len(statuses)]

    change_status(token, status, current_status)

    status_count += 1

    time.sleep(speed_rotator)
