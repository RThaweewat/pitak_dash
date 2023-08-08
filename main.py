import streamlit as st
import pandas as pd
import datetime
import numpy as np
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

# Convert pandas Timestamps to native datetime objects
times = (
    data["time"]
    .apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    .unique()
)
times = sorted(times)

selected_index = st.slider("Choose a time:", min_value=0, max_value=len(times)-1, value=0)
selected_time = times[selected_index]
time_range = selected_time.strftime('%Y-%m-%d %H:%M:%S')

filtered_data = data[data["time"] == time_range]

m = folium.Map(location=[13.6773, 100.4554], zoom_start=14, tiles="OpenStreetMap")

for no_board, coord in location_dict.items():
    lat, long = coord[0], coord[1]

    board_data = data[(data['time'] == time_range) & (data['no_board'] == no_board)]
    if not board_data.empty:
        value = board_data[feature].values[0]
        # Assuming you have a function named color_mapper() which returns a color based on the value
        folium.CircleMarker(
            location=[lat, long],
            radius=10,
            popup=f"Board: {no_board}, {feature}: {value}",
            fill=True,
            fill_color=color_mapper(value),
            fill_opacity=0.6,
        ).add_to(m)

folium_static(m)
