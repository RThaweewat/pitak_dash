import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap
import re


# Load data
@st.cache
def load_data():
    return pd.read_csv("result.csv")


data = load_data()

# Streamlit UI
st.title("Interactive Heat Map on Folium")

feature = st.selectbox(
    "Choose a feature to plot:", ["temperature", "humidity", "gas_smoke", "proba"]
)

# Get unique times and create a time range dropdown
times = sorted(data["time"].unique())
start_time = st.selectbox('Select start time:', times, index=0, key="start_time")
end_time = st.selectbox('Select end time:', times, index=len(times)-1, key="end_time")
filtered_data = data[(data["time"] >= start_time) & (data["time"] <= end_time)]

# Ensure that the end time is always after the start time
if start_time >= end_time:
    st.warning("End time must be after start time!")
    st.stop()

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
    Board No: {round(index, 2)}<br>
    Temperature: {round(row['temperature'], 2)}°C<br>
    Humidity: {round(row['humidity'], 2)}%<br>
    Risk Probability: {round(row['proba'], 2)}
    """

    folium.Marker(
        [lat, long],
        popup=popup_content,
    ).add_to(m)

# Add heatmap
HeatMap(heatmap_data, radius=20).add_to(m)
folium_static(m)
