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

st.subheader("Risk Map")

# Ensure that the end time is always after the start time
if start_time >= end_time:
    st.warning("End time must be after start time!")
    st.stop()

filtered_data = data[(data["time"] >= start_time) & (data["time"] <= end_time)]

# Average risk (assuming 'proba' column represents risk)
average_risk = filtered_data["proba"].mean()
st.write(f"Average risk for selected time period: {average_risk}")

token = "pk.eyJ1IjoidGhhd2Vld2F0IiwiYSI6ImNrbzM0bHEycTA3YzMybm9udzlnazdobGsifQ.NwdYPk_pQDYenDfIsdyatg"  # your mapbox token
tileurl = (
    "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token="
    + str(token)
)
attr = "© Mapbox © OpenStreetMap"

m = folium.Map(
    location=[13.6773, 100.4555], zoom_start=21, tiles=tileurl, attr=attr, max_zoom=30
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
    <b>Board No:</b> {index}<br>
    <b>Temperature:</b> {row['temperature'].round(2)}°C<br>
    <b>Humidity:</b> {row['humidity'].round(2)}%<br>
    <b>Risk Probability:</b> {row['proba'].round(2)}
    """

    folium.Marker(
        [lat, long],
        popup=popup_content,
    ).add_to(m)

# Add heatmap
heatmap = HeatMap(
    heatmap_data,
    radius=50,
    blur=50,
    gradient={0.2: "blue", 0.4: "lime", 0.6: "orange", 1: "red"},
).add_to(m)

folium_static(m)

# title for streamlit line chart
st.subheader("Risk Probability over Time")
st.line_chart(filtered_data.set_index("time")["proba"])

# display smoke and fire image split half layout 2 images in one row
st.subheader("Smoke and Fire Image")

col1, col2 = st.columns(2)

# get current time
now = datetime.datetime.now()
current_time = now.strftime("YYYY-MM-DD HH:MM:SS")

with col1:
    st.caption(f"Smoke Detection @ {str(current_time)}")
    st.image("smoke_predict.jpg")

with col2:
    st.caption(f"Fire Detection @ {str(current_time)}")
    st.image("fire_predict.jpg")
