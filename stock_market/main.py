# API for retrieving stock market prices

import os
import requests

import json
import datetime
import smtplib
import html

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
threshold_limit = 0.01


def print_news(news, num_news):
    msg = []
    for num in range(num_news):
        msg.append("News num " + str(num+1) + "\n" +
                   "Title: " + html.unescape(data_news.json()["articles"][num]["title"]) + "\n" +
                   "Brief: " + html.unescape(data_news.json()["articles"][num]["description"]) + "\n")
    print("".join(msg))
    return msg

#------ Retrieving stock price --------#

# Getting the API key from the environment variables.
api_key_alpha = os.environ.get("API_KEY_ALPHA_VANTAGE")

# Making the request
url = "https://www.alphavantage.co/query"
function = "TIME_SERIES_DAILY"
symbol = STOCK
params = {
    "function": function,
    "symbol": symbol,
    "apikey": api_key_alpha,
}
data = requests.get(url, params=params)

#------ Checking changes within last two days --------#

day_0 = str(datetime.date.today() - datetime.timedelta(days=2))

n = 1
while True:
    try:
        day_1 = str(datetime.date.today() - datetime.timedelta(days=n))
        close_day_1 = float(data.json()["Time Series (Daily)"][day_1]["4. close"])
    except KeyError:
        n += 1
        pass
    else:
        break

while True:
    try:
        day_0 = str(datetime.date.today() - datetime.timedelta(days=n + 1))
        close_day_0 = float(data.json()["Time Series (Daily)"][day_0]["4. close"])
    except KeyError:
        n += 1
        pass
    else:
        break


close_day_0 = float(data.json()["Time Series (Daily)"][day_0]["4. close"])

print(f"Closing on {day_1}: {close_day_1}")
print(f"Closing on {day_0}: {close_day_0}")
print((close_day_1 - close_day_0)/close_day_1)
if abs(close_day_1 - close_day_0)/close_day_1 > threshold_limit:
    print("Here are the headlines of the first three news:")

#------ Retriving the last three news from the company -----#
    api_key_news = os.environ.get("API_KEY_NEWS")

    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": api_key_news,
        "q": COMPANY_NAME,
        "searchin": "title",
        "from": day_1,
        "to": day_1,
        "language": "en",
    }
    data_news = requests.get(url, params=params)
    # print(json.dumps(data_news.json(), indent=4))
    msg = print_news(data_news.json()["articles"], 3)

#------ Sending email with news -----#
    email_sender = os.environ.get("EMAIL_SENDER")
    email_target = os.environ.get("EMAIL_TARGET")
    email_pass = os.environ.get("EMAIL_PASS")

    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=email_sender, password=email_pass)
    msg_txt = "Subject: Stock Report\n\n" + "".join(msg)
    msg_txt = msg_txt.encode("utf-8")
    connection.sendmail(
        from_addr=email_sender,
        to_addrs=email_target,
        msg=msg_txt,
    )
    connection.close()

#print(json.dumps(data.json(), indent=4, sort_keys=True))


