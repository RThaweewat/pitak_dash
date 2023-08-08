import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap
import re


def dms_to_decimal(dms_lat, dms_long):
    """Convert DMS (Degrees, Minutes, Seconds) to decimal format for latitude and longitude."""
    def dms2dd(dms):
        degrees, minutes, direction = 0, 0, 1
        dms_match = re.match(r'(\d+)°(\d+)\'([\d.]+)"([NSEW])', dms)
        if dms_match:
            degrees = float(dms_match.group(1))
            minutes = float(dms_match.group(2))
            seconds = float(dms_match.group(3))
            if dms_match.group(4) in ['S', 'W']:
                direction = -1
        return direction * (degrees + minutes/60 + seconds/3600)

    lat = dms2dd(dms_lat)
    long = dms2dd(dms_long)
    return lat, long


@st.cache_data
def load_data():
    return pd.read_csv("result.csv")


data = load_data()

location_dict = {
    1: ["13°40'38.3\"N", "100°27'19.6\"E"],
    2: ["3°40'38.5\"N", "100°27'19.6\"E"],
    3: ["13°40'38.5\"N", "100°27'19.8\"E"],
    4: ["13°40'38.3\"N", "100°27'19.8\"E"],
}

# Convert the location_dict to decimal
for key, coords in location_dict.items():
    location_dict[key] = dms_to_decimal(coords[0], coords[1])

# Streamlit UI
st.title("Interactive Heat Map on Folium")

feature = st.selectbox(
    "Choose a feature to plot:", ["temperature", "humidity", "gas_smoke", "proba"]
)

# Get unique times and create a time range dropdown
times = sorted(data["time"].unique())
time_range = st.selectbox('Select time period:', times)

filtered_data = data[data["time"] == time_range]

# Average risk (assuming 'proba' column represents risk)
average_risk = filtered_data['proba'].mean()
st.write(f"Average risk for selected time: {average_risk}")

m = folium.Map(location=[13.6773, 100.4554], zoom_start=14, tiles="OpenStreetMap")

heatmap_data = []

for no_board, coord in location_dict.items():
    lat, long = coord[0], coord[1]
    board_data = data[(data['time'] == time_range) & (data['no_board'] == no_board)]
    if not board_data.empty:
        value = board_data[feature].values[0]
        heatmap_data.append([lat, long, value])

# Add heatmap
HeatMap(heatmap_data, radius=25).add_to(m)
folium_static(m)