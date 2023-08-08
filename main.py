# streamlit_app.py
import streamlit as st
import pandas as pd
import datetime
import numpy as np
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap


# Load data
@st.cache_data
def load_data():
    return pd.read_csv("result.csv")


data = load_data()

# Convert the location_dict to degrees
location_dict = {
    1: ["13°40'38.3\"N", "100°27'19.6\"E"],
    2: ["3°40'38.5\"N", "100°27'19.6\"E"],
    3: ["13°40'38.5\"N", "100°27'19.8\"E"],
    4: ["13°40'38.3\"N", "100°27'19.8\"E"],
}


def dms_to_dd(dms):
    degrees, minutes, direction = (
        int(dms.split("°")[0]),
        float(dms.split("°")[1].split("'")[0]),
        dms.split("'")[-1],
    )
    dd = degrees + minutes / 60.0
    if direction in ["S", "W"]:
        dd *= -1
    return dd


for key, coords in location_dict.items():
    location_dict[key] = [dms_to_dd(coords[0]), dms_to_dd(coords[1])]

# Streamlit UI
st.title("Interactive Heat Map on Folium")

# Dropdown menu
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

# Set the slider to select an index
selected_index = st.slider("Choose a time:", min_value=0, max_value=len(times)-1, value=0)

# Get the selected time based on the index
selected_time = times[selected_index]
time_range = selected_time.strftime('%Y-%m-%d %H:%M:%S')


filtered_data = data[data["time"] == time_range]

m = folium.Map(location=[13.6773, 100.4554], zoom_start=15)

# Create HeatMap
heat_data = [
    [row["lat"], row["long"], row[feature]] for index, row in filtered_data.iterrows()
]
HeatMap(heat_data).add_to(m)

# Display Folium map with Streamlit
folium_static(m)

if __name__ == "__main__":
    st.run()
