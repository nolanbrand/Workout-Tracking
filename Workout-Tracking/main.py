import requests
import datetime
import os

GENDER = "Male"
WEIGHT_KG = "66"
HEIGHT_CM = "179"
AGE = "32"

API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
GOOGLE_SHEETS_API = os.environ["GOOGLE_SHEETS_API"]
BASIC_AUTHORIZATION_KEY = os.environ["BASIC_AUTHORIZATION_KEY"]

user_input = input("What exercise did you do?: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Authorization": BASIC_AUTHORIZATION_KEY,
}

params = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=API_ENDPOINT, json=params, headers=headers)
data = response.json()

exercises = data["exercises"]

for i in range(len(exercises)):
    exercise = exercises[i]["name"].title()
    duration = exercises[i]["duration_min"]
    calories = exercises[i]["nf_calories"]

    current_time = datetime.datetime.now()
    date = current_time.strftime("%m/%d/%Y")
    time = current_time.strftime("%H:%M:%S")

    add_to_sheets = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
            }
    }

    to_sheets = requests.post(url=GOOGLE_SHEETS_API, json=add_to_sheets, headers=headers)

