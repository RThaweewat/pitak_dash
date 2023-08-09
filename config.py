import os
import sys
from pathlib import Path


# Base Directory
BASE_DIR = Path(__file__).parent
PARENT_DIR = BASE_DIR.parent

# Make folders at raw_img directory
RAW_IMG = Path(PARENT_DIR, "raw_img")
RAW_IMG.mkdir(parents=True, exist_ok=True)
RAW_IMG_PATH = str(RAW_IMG)

# Make folders at raw_img directory
MODEL_PATH = Path(PARENT_DIR, "model")
MODEL_PATH.mkdir(parents=True, exist_ok=True)
MODEL_PATH_STR = str(MODEL_PATH)

# Make predict img directory
PREDICT_IMG = Path(PARENT_DIR, "predict_img")
PREDICT_IMG.mkdir(parents=True, exist_ok=True)
# get image path of predict_img
PREDICT_IMG_PATH = str(PREDICT_IMG)