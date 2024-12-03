# This code finds cheap flights once a day.

import json
import requests

# ------ Reading the travel details ----- #
with open('travel_details.json', 'r') as travel_file:
    data = json.loads(travel_file.read())

# ----- Requesting flight details ------ #
url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v1/prices/cheap"
params = {
    "origin": "MED",
    "page": "None",
    "currency": "SEK",
    "destination": "ARN"}

headers = {
	"X-Access-Token": "undefined",
	"X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com",
	"X-RapidAPI-Key": "fe7f90dc61msh7c1d0d22c80bd12p13fa04jsnee2d1be3d6f1"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

# TODO: request to flight search engine


#  TODO: send email maraljure_reports@gmail.com

# TODO: Read the destinations and travel details

# TODO: loop over the request within the travel days

# TODO: compare with the target price each query. If lower, send email.

# TODO: send to the cloud with python anywhere