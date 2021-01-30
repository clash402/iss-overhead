import requests as req
import smtplib
import time
from datetime import datetime


# PROPERTIES
MY_EMAIL = ""
MY_PASSWORD = ""
MY_LAT = 0
MY_LON = 0


# ISS METHODS
def check_for_iss(lat, lon, my_email, my_password):
    if iss_is_overhead(lat, lon) and is_night(lat, lon):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg="Subject:Look Up!\n\nThe ISS is above you in the sky!"
            )


def iss_is_overhead(lat, lon):
    (iss_lat, iss_lon) = get_iss_location()
    if lat - 5 <= iss_lat <= lat + 5 and lon - 5 <= iss_lon <= lon + 5:
        return True


def is_night(lat, lon):
    (sunrise, sunset) = get_sun_location(lat, lon)
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


# DATA MANAGER
def get_iss_location():
    res = req.get(url="http://api.open-notify.org/iss-now.json")
    res.raise_for_status()
    data = res.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_lon = float(data["iss_position"]["longitude"])

    return iss_lat, iss_lon


def get_sun_location(lat, lon):
    params = {"lat": lat, "lng": lon, "formatted": 0}
    res = req.get("https://api.sunrise-sunset.org/json", params=params)
    res.raise_for_status()
    data = res.json()

    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])

    return sunrise, sunset


# MAIN
def start():
    app_is_running = True
    while app_is_running:
        check_for_iss(MY_LAT, MY_LON, MY_EMAIL, MY_PASSWORD)
        time.sleep(60)


start()
