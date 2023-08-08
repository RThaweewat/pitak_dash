import streamlit as st
import pandas as pd
from folium.plugins import HeatMap
import folium
import time
from datetime import datetime, timedelta


@st.cache_data
def load_data():
	df = pd.read_csv('result.csv')
	df['time'] = pd.to_datetime(df['time'])
	df['timestamp'] = df['time'].dt.floor('T')
	df.set_index('time', inplace=True)
	return df


df = load_data()

selected_parameter = st.selectbox('Select parameter for heatmap', ['temperature', 'humidity', 'gas_smoke', 'proba'])

start_time = st.slider("Move slider to change the hour", value=0, max_value=23)

min_time = datetime.now().replace(hour=start_time, minute=0, second=0)
max_time = min_time + timedelta(hours=1)

df = df[(df.index >= min_time) & (df.index <= max_time)]

if st.button('Generate HeatMap'):
	m = folium.Map([13.677305, 100.455444], zoom_start=14)

	data = df[['no_board', 'lat', 'long', selected_parameter]].groupby(['no_board']).mean().reset_index().values.tolist()

	# plot heatmap
	HeatMap(data).add_to(m)

	folium_display=m._repr_html_()

	st.markdown(folium_display,unsafe_allow_html=True)
