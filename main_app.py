import requests
import os
import sys
from pathlib import Path
import datetime
from src.fit_smoke import run_smoke
from src.fit_fire import run_fire
from roboflow import Roboflow
from config import RAW_IMG, PREDICT_IMG_PATH, RAW_IMG_PATH

# get current date and time YYYY_MM_DD_HH_MM_SS
now = datetime.datetime.now()
current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

url = 'http://192.168.4.1/capture'

# loop response = requests.get(url) for 4 times
for i in range(4):
    response = requests.get(url)

if not os.path.exists(RAW_IMG):
    os.makedirs(RAW_IMG)

if response.status_code == 200:
    print("writing image...")
    PATH_FILE = os.path.join(RAW_IMG, f"img_raw_{current_time}.jpg")
    with open(PATH_FILE, "wb") as f:
        content = response.content
        f.write(content)
        print("Finish writing image...")

run_smoke(RAW_IMG_PATH, PREDICT_IMG_PATH, current_time)
run_fire(RAW_IMG_PATH, PREDICT_IMG_PATH, current_time)

print("Finish running smoke...")
