import time

import requests
from datetime import datetime
import smtplib
MY_LAT = 37.718926 # Your latitude
MY_LONG = 30.248454 # Your longitude
MY_EMAIL = "karabas.berko@gmail.com"
MY_PASSWORD = "izwnafpjlgmbqmgm"
def is_iss_head():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if iss_longitude - 5 < MY_LONG or iss_longitude+5 > MY_LONG and iss_latitude -5 < MY_LAT or iss_latitude+5>MY_LAT:
        return True
#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}
def is_night():

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])+3
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])+3

    time_now = datetime.now()
    if time_now.hour > sunset and time_now.hour > sunrise:
        return True
while True:
    time.sleep(60)
    if is_iss_head() and is_night():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL,MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="berkay.karabas091@gmail.com",
                                msg="Subject:ISS close your location\n\nLook up!")
#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



