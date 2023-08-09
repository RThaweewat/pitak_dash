import pandas as pd
import numpy as np
import json
from xgboost import XGBClassifier
from config import MODEL_PATH_STR

# pandas setting flaot format
pd.options.display.float_format = "{:.2f}".format


def get_data(file_path):
    """
    :return: A pandas dataframe with the data from the csv file.
    """
    return pd.read_csv(file_path)


def transform_date(raw_data: pd.DataFrame, distance_value):
    select_cols = [
        "time",
        "no_board",
        "gas_smoke",
        "temperature",
        "humidity",
    ]
    raw_data["time"] = pd.to_datetime(raw_data["time"]) + pd.Timedelta(hours=7)
    raw_data["distance"] = distance_value
    return raw_data[select_cols]


def resample(raw_data: pd.DataFrame):
    return (
        raw_data.set_index("time")
        .resample("1S")
        .ffill()
        .fillna(method="bfill")
        .reset_index()
    )


def feature_engineering(raw_data: pd.DataFrame):
    """
    Perform feature engineering on raw data.

    :param raw_data: The raw dataset to perform feature engineering on.
    :type raw_data: pd.DataFrame
    :return: The dataset with engineered features.
    :rtype: pd.DataFrame
    """
    # loop lag 1-10
    for i in range(1, 31):
        raw_data['gas_smoke_lag' + str(i)] = raw_data['gas_smoke'].shift(i)

    # loop moving average 1-10
    for i in range(1, 31):
        raw_data['gas_smoke_ma' + str(i)] = raw_data['gas_smoke'].rolling(window=i).mean()

    return raw_data

"""
raw_data = get_data(path)
raw_data = transform_date(raw_data, 1)
raw_data = resample(raw_data)
raw_data = feature_engineering(raw_data)

# load xgboost model from json
model_path = f"{MODEL_PATH_STR}\\fire.json"

with open(model_path, "r") as f:
    model = XGBClassifier()
    model.load_model(model_path)

# predict
y_pred = model.predict(raw_data)
print(y_pred)
"""
