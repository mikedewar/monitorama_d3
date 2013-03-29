import requests
import json
import time
import random
import string

def click_generator():
    while True:
        yield {
            "a": ''.join(random.sample(string.ascii_letters, 10)),
            "c": "NZ",
            "tz": "Pacific/Auckland",
            "gr": "E7",
            "g": "4dwBHm",
            "h": "KeNAvr",
            "l": "nasatwitter",
            "al": "en-us",
            "hh": "go.nasa.gov",
            "r": "http://t.co/8HMEs0hZ7c",
            "u": "http://apod.nasa.gov/apod/astropix.html",
            "t": 1364499595,
            "hc": 1336137728,
            "cy": "Auckland",
            "ll": [ random.uniform(-90, 90), random.uniform(-180,180)]
        }

# deal with each line as it comes in
for data in click_generator():
    line = json.dumps(data)
    requests.post('http://127.0.0.1:8888/put',data=line)
    time.sleep(1)
