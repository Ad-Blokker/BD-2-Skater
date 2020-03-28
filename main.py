
# Imports
import streamlit as st
import requests 
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from bokeh.plotting import figure


# Api
URL =  "https://speedskatingresults.com/api/json/skater_results.php"

SkaterID = 1195
Distance = 500
Season = 2012

Parameters = {'skater':SkaterID, 'distance':Distance, 'season': Season} 

r = requests.get(url = URL, params = Parameters) 

data = r.json() 

# Json to dataframe
from pandas.io.json import json_normalize
df = json_normalize(data)

# Json column to new dataframe
dfCompetitions = pd.io.json.json_normalize(df.results[0])

dfCompetitions.drop(columns=['link'])

# to numeric
dfCompetitions['time'] = dfCompetitions['time'].str.replace(',','.')
dfCompetitions['time'] = pd.to_numeric(dfCompetitions['time'])

st.title("Gemiddelde snelheid")
st.header("Info:") 
st.write("SkaterID: " + str(SkaterID) + "   \nSeason: " + str(Season))

data = []
dataSpeed = []
dataIndex = []

for index, row in dfCompetitions.iterrows():
    strindex = str(index + 1)

    time = dfCompetitions['time'].iloc[index]
    speedEach = Distance / time
    dataSpeed.append(speedEach)
    dataIndex.append(index)
    data.append([strindex, speedEach])
    
cols = ['id', 'speed']

dfSpeed = pd.DataFrame(data, columns=cols)

fig = figure(
    title = 'Speed of ' +str(Distance) + "m",
    x_axis_label='Amount of runs',
    y_axis_label='Speed in km/h'
)

fig.line(dfSpeed['id'], dfSpeed['speed'], legend='Speed', line_width=2)

st.bokeh_chart(fig, use_container_width=True)
