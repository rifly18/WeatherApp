import smtplib, ssl
import os
import requests
password = ""
my_email = ""
to_email = ""
# Create a secure SSL context




subscriberList ={}

account_sid = ''
auth_token = ''

api_key = ""


LAT = 55.396229
LONG = 10.390600

parameters = {
        "lat": LAT,
        "lon": LONG,
        "appid": api_key,
        "exclude": "current,minutely,daily"

    }
response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
    # print(weather_data)
weather_slice = weather_data["hourly"][:12]  # Går fra 1 til 12.

will_rain = False
for hour_Data in weather_slice:
    condition_code = hour_Data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    for subscribers in subscriberList:
        with smtplib.SMTP("smtp.gmail.com") as server:
            server = smtplib.SMTP("smtp.gmail.com")
            server.starttls()
            server.login(user=my_email, password=password)
            server.sendmail(from_addr=my_email,
                                to_addrs=subscriberList[subscribers],
                                msg=f"Subject: Hej {subscribers}. Det kommer til at regne")
else:
    with smtplib.SMTP("smtp.gmail.com") as server:
        server = smtplib.SMTP("smtp.gmail.com")
        server.starttls()
        server.login(user=my_email, password=password)
        for subscribers in subscriberList:
            server.sendmail(from_addr=my_email,
                            to_addrs=subscriberList[subscribers],
                            msg=f"Subject: Hej {subscribers}. Det kommer IKKE til at regne")
