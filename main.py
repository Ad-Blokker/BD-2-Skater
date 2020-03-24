
# Imports
import streamlit as st
import requests 
import pandas as pd
import plotly.graph_objs as go
import numpy as np

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

# Calculations
Total = dfCompetitions['time'].sum()
Count = dfCompetitions['time'].count()
Avg = (Total/Count) * 60
Speed = Avg/Distance
SpeedString = str("%.2f" % Speed)


st.title("Gemiddelde snelheid")
st.header("Info:") 
st.write("SkaterID: " + str(SkaterID) + "   \nSeason: " + str(Season) + "\nGemiddelde snelheid: " + SpeedString)


# print("Seizoen: " + str(Season))
# print("Gemiddelde m/s: " + SpeedString)



