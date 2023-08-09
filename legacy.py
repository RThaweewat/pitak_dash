import requests
import os
import sys
# import macwifi
# import time

def checkSysPathAndAppend(path, stepBack = 0):
    if stepBack > 0:
        for istep in range(stepBack):
            if istep == 0:
                pathStepBack = path
            pathStepBack, filename = os.path.split(pathStepBack)
    else:
        pathStepBack = path

    if not pathStepBack in sys.path:
        sys.path.append(pathStepBack)

    return pathStepBack

folderFile, filename = os.path.split(os.path.realpath(__file__))

# Make folders at root directory
MODELS_DIR = Path(PARENT_DIR, "models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)
FOLDER_PROJECT = checkSysPathAndAppend(folderFile, 2)

FOLDER_IMAGE = os.path.join(FOLDER_PROJECT, 'Images', 'RemoteOCR_01_test')
url = 'http://192.168.4.1/capture'
filename = f'test.jpg'

print('requesting...')
response = requests.get(url)

if not os.path.exists(FOLDER_IMAGE):
    os.makedirs(FOLDER_IMAGE)

if response.status_code == 200:   
    PATH_FILE = os.path.join(FOLDER_IMAGE, filename)  
    with open(PATH_FILE, 'wb') as f:
        content = response.content
        print("writing image...")
        f.write(content) 
