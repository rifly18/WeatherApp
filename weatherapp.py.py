import numpy as np
import requests
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

addresser = {}
weekno = datetime.today().weekday()
if weekno < 5:
    addresser = {"Ricco":["Vesterbro 70,Denmark,5000","ricco_noe@hotmail.com"],
                 "Pia og Frank":["Kløvermarken 48, Denmark, 5492","piaogfrank@os.dk"],
                 "Michael Knudsen":["Hvepsevej, Denmark,9000","mich989d@hotmail.com"],
                 "Louise Sjodsholm":["Vesterbro 70, Denmark,5000","louise@sjodsholm.dk"]}

    api_key = "3ced7307699853aed2cb4bab76662070"
    email = "riccoprogrammering@gmail.com"
    passw = "Qwertgfdsa123"

    now = datetime.now()
    now =int(str(now).split(" ")[1].split(":")[0])
    for key,value in addresser.items():
        will_rain = False
        i = 0
        whenRain = []
        strings = ""
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(value[0]) +'?format=json'
        response = requests.get(url).json()

        LAT = response[0]['lat']
        LONG = response[0]['lon']

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
        weather_slice = weather_data["hourly"][:12]  # Går fra 1 til 12. (fra 0-11)
        for hour_Data in weather_slice:
            condition_code = hour_Data["weather"][0]["id"]
            if int(condition_code) < 700:
                will_rain = True
                whenRain.append(True)
            else:
                whenRain.append(False)
        for each in range(len(whenRain)):
            if whenRain[each] == True:
                strings = strings + f"{now + each}: regner IKKE\n"

            else:
                strings  = strings + f"{now + each}: regner IKKE\n"

        message = MIMEMultipart()
        message['From'] = email
        message['To'] = value[1]
        message['Subject'] = f"Hej {key}, her er din daglige opdatering på vejret"

        message.attach(MIMEText(strings))
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(email, passw)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(email, value[1], text)
        session.quit()
        print('Mail Sent')
else:
    "Weekend, no email"