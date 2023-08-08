import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap

# Load data
@st.cache
def load_data():
    return pd.read_csv("result.csv")

data = load_data()

# Create a time input widget for start and end times with minute precision
start_time = st.time_input('Select start time:', datetime.time(0, 0)).strftime('%H:%M')
end_time = st.time_input('Select end time:', datetime.time(23, 59)).strftime('%H:%M')

# Filter data based on the chosen times
filtered_data = data[(data["time"].str.slice(0, 5) >= start_time) & (data["time"].str.slice(0, 5) <= end_time)]

# Streamlit UI
st.title("Interactive Heat Map on Folium")

# Dropdown menu
feature = st.selectbox(
    "Choose a feature to plot:", ["temperature", "humidity", "gas_smoke", "proba"]
)

m = folium.Map(location=[13.6771, 100.453], zoom_start=20, tiles="OpenStreetMap", max_zoom=30)

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
