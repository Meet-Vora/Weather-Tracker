import api_key
import requests
import json
from datetime import datetime
# from tabulate import tabulate

API_KEY = api_key.get_api_key()
LAT, LON = api_key.get_lat_lon()
UNITS = "imperial"

# data = {}


def get_weather():
    file_data = load_data()
    data = get_data(file_data["hourly"])
    print_data(data)
    print("\nIS PLAYABLE:", is_playable(data))


def get_data(hourly_data):
    # with open("response.json", "r") as file:
    #     file_data = json.load(file)
    data = {}
    for i in range(len(hourly_data)):
        entry = hourly_data[i]
        timestamp = datetime.utcfromtimestamp(entry["dt"])
        # print(timestamp.hour)
        data[i] = {
            "time": timestamp.hour,
            "temperature": entry["temp"],
            "precipitation chance": entry["pop"],
            "wind speed": entry["wind_speed"]
        }
    return data

    # print(data)
    # print("1", str(date_time.month) + "/" + str(date_time.day))
    # print("2", date_time.hour)
    # print('test')


def load_data():
    url = "https://api.openweathermap.org/data/2.5/onecall?" \
        "lat={0}&lon={1}&units={2}&appid={3}".format(LAT, LON, UNITS, API_KEY)

    response = requests.get(url)
    file_data = None
    with open("response.json", "w") as outfile:
        json.dump(response.json(), outfile)

    with open("response.json", "r") as infile:
        file_data = json.load(infile)

    return file_data


def is_playable(data):
    for value in data.values():
        if value['precipitation chance'] > 0:
            return False
        if value['wind speed'] > 12:
            return False
    return True


# get data for 12 hours, from midnight to noon the next day
# need it to print out in a table:
# ########################################
# hour | % precipitation | wind speed (mph)
# ########################################

# print output
def print_data(data):
    print("{:<8} {:<15} {:<10} {:<10}".format(
        "Hour", "Temp", "% Precip", "Wind Speed"))

    for v in data.values():
        time, temp, precip, wind_speed = v["time"], v["temperature"], v["precipitation chance"], v["wind speed"]
        print("{:<8} {:<15} {:<10} {:<10}".format(
            time, temp, precip, wind_speed))
    # print(tabulate(data, headers=["Hour", "Temp", "% Precip", "Wind Speed"]))


get_weather()
