from main import get_bulb
from time import sleep
import requests

bulb = get_bulb()

def get_rate(base="BTC", currency="USD"):
    r = None
    res = requests.get(f"https://api.coinbase.com/v2/prices/{currency}/spot")
    data = res.json()["data"]
    for i in data:
        if i["base"] == base:
            r = i["amount"]
            break
    return r

rate = get_rate()

def track_rate():
    global rate
    new_rate = get_rate()
    if new_rate < rate:
        bulb.set_rgb(255, 0, 0)
    elif new_rate > rate:
        bulb.set_rgb(0, 255, 0)
    else:
        bulb.set_rgb(70, 70, 70)

    rate = new_rate

for i in range(100):
    track_rate()
    print(rate)
    sleep(5)
    

bulb.set_rgb(50, 50, 50)