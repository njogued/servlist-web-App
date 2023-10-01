import requests
import time

while True:
    response = requests.get("https://servlist.onrender.com/")
    if response.status_code == 200:
        print("ping")
    else:
        print("Error code:", response.status_code)
    time.sleep(600)
