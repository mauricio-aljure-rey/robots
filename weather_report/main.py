# Weather forecast with yr 

import requests
import json
# import pywhatkit
import flask


# Rådsparken information
lat_radsparken = 59.2409
lon_radsparken = 17.9870

# Stockholm information
lat_stock = 59.329
lon_stock = 18.069

lat = lat_radsparken
lon = lon_radsparken


# Open Weather configuration
API_key = "4c0855da321c0d905dc62f6e3a6c8cff"
ow_endpoint = f"https://api.openweathermap.org/data/3.0/onecall"
ow_param = {
    "lat": lat,
    "lon": lon,
    "appid": API_key
}

# yr configuration
yr_endpoint = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
yr_param = {
    "lat": lat,
    "lon": lon,
}
yr_headers = {
    'User-Agent': 'learning_python',
    'From': 'nonworking@email.com',
}

endpoint = {
    "endpoint": yr_endpoint,
    "params": yr_param
}

answer = requests.get(endpoint["endpoint"], params=endpoint["params"], headers=yr_headers)

data = answer.json()
# Obtaining a list of dictionaries, hour by hour.
# First key is "time" in format "2022-05-21T13:00:0ZZ" 0
# Key "data" is a dictionary with dictionaries.
data = data["properties"]["timeseries"]
print(json.dumps(data, indent=3))

# Creating a new list of dictionaries with the information from the precipitation only.
next_hour_rain_data = []
for idx, item in enumerate(data):
    try:
        next_hour_rain_data.append({
            "time": item["time"],
            "precipitation_amount": item["data"]["next_1_hours"]["details"]["precipitation_amount"],
        })
    except KeyError:
        pass

# Going through the data and collecting when it is raining.
raining_at = []
for item in next_hour_rain_data:
    if item["precipitation_amount"] > 0:
        raining_at.append({
            "day": item["time"].split("T")[0],
            "hour": item["time"].split("T")[1][0:2],
            "amount": item["precipitation_amount"]
        })

# print(json.dumps(raining_at, indent=3))

if raining_at:
    print("It is going to rain.")
else:
    print("It is not going to rain at all!")

# print(json.dumps(next_hour_rain_data, indent=2))
# print(json.dumps(next_hour_rain_data, indent=2))
