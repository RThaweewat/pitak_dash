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
    4: ["13°40'38.3\"N", "100°27'19.8\"E"]
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
start_time = st.selectbox('Select start time:', times, index=0, key="start_time")
end_time = st.selectbox('Select end time:', times, index=len(times)-1, key="end_time")


# Ensure that the end time is always after the start time
if start_time >= end_time:
    st.warning("End time must be after start time!")
    st.stop()

filtered_data = data[(data["time"] >= start_time) & (data["time"] <= end_time)]

# Average risk (assuming 'proba' column represents risk)
average_risk = filtered_data['proba'].mean()
st.write(f"Average risk for selected time period: {average_risk}")

# Filter data based on the chosen times
filtered_data = data[(data["time"].str.slice(0, 5) >= start_time) & (data["time"].str.slice(0, 5) <= end_time)]

# Streamlit UI
st.title("Interactive Heat Map on Folium")

m = folium.Map(location=[13.6771, 100.455], zoom_start=20, tiles="OpenStreetMap", max_zoom=30)

heatmap_data = []

# Loop to add board data to heatmap_data list for the chosen time period and add clickable markers
for index, row in filtered_data.groupby('no_board').mean().iterrows():  # Grouping by no_board and taking mean values
    lat, long = row['lat'], row['long']
    value = row[feature]
    heatmap_data.append([lat, long, value])

    popup_content = f"""
    Board No: {index}<br>
    Temperature: {row['temperature']}°C<br>
    Humidity: {row['humidity']}%<br>
    Risk Probability: {row['proba']}
    """

    folium.Marker(
        [lat, long],
        popup=popup_content,
    ).add_to(m)

# Add heatmap
HeatMap(heatmap_data, radius=20).add_to(m)
folium_static(m)
