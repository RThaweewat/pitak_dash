import streamlit as st
import pandas as pd
import datetime
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap


@st.cache_data()
def load_data():
    return pd.read_csv("result_m.csv")


data = load_data()

# Streamlit UI
st.title("Pitak Risk-Map")

feature = st.selectbox(
    "Choose a feature to plot:", ["temperature", "humidity", "gas_smoke", "proba"]
)

# Get unique times and create a time range dropdown
times = sorted(data["time"].unique())
start_time = st.selectbox("Select start time:", times, index=0, key="start_time")
end_time = st.selectbox("Select end time:", times, index=len(times) - 1, key="end_time")

# Ensure that the end time is always after the start time
if start_time >= end_time:
    st.warning("End time must be after start time!")
    st.stop()

filtered_data = data[(data["time"] >= start_time) & (data["time"] <= end_time)]

# Average risk (assuming 'proba' column represents risk)
average_risk = filtered_data["proba"].mean()
st.write(f"Average risk for selected time period: {average_risk}")

m = folium.Map(
    location=[13.6773, 100.4555], zoom_start=21, tiles="OpenStreetMap", max_zoom=30
)

heatmap_data = []

# Instead of directly computing mean after grouping, select necessary columns first
numeric_cols = ["lat", "long", "temperature", "humidity", "gas_smoke", "proba"]
grouped_data = filtered_data.groupby("no_board")[numeric_cols].mean()

# Loop to add board data to heatmap_data list for the chosen time period and add clickable markers
for index, row in grouped_data.iterrows():
    lat, long = row["lat"], row["long"]
    value = row[feature]
    heatmap_data.append([lat, long, value])

    popup_content = f"""
    **Board No:** {index}<br>
    **Temperature:** {row['temperature'].round(2)}°C<br>
    **Humidity:** {row['humidity'].round(2)}%<br>
    **Risk Probability:** {row['proba'].round(2)}
    """

    folium.Marker(
        [lat, long],
        popup=popup_content,
    ).add_to(m)

# Add heatmap
HeatMap(heatmap_data, radius=30).add_to(m)
folium_static(m)

# title for streamlit line chart
st.title("Risk Probability")
st.line_chart(filtered_data.set_index("time")["proba"])
