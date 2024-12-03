# Amazon tracking program that sends email once a product has reaached a desired value.

import json
import requests
import bs4
import smtplib
import os

# Loading json file with products from mediamarkt
with open("product_info.json") as file:
    products = json.load(file)
products = products["products"]

# Scrapping MediaMarkt searching for price
for item in products:
    item_name = item["name"]
    link = item["url"]
    price_target = item["target_price"]
    response = requests.get(link) # Reading the webpage
    soup = bs4.BeautifulSoup(response.text, "html.parser") # Getting the webpage content
    price_info = soup.find_all("meta", itemprop="price")[0]["content"]
    print(price_info)
    if int(price_info) <= int(price_target): # Time to send an email
        email_sender = os.environ.get("EMAIL_SENDER")
        email_target = os.environ.get("EMAIL_TARGET")
        email_pass = os.environ.get("EMAIL_SENDER_PASS")
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=email_sender, password=email_pass)
            msg = f"MediaMarkt item {item_name} is on target price. Check it on:\n" \
                  f"{link}"
            msg_txt = f"Subject: Price Alert: {item_name}\n\n" + msg
            msg_txt = msg_txt.encode("utf-8")
            connection.sendmail(
                from_addr=email_sender,
                to_addrs=email_target,
                msg=msg_txt,
            )
