# Imports
import streamlit as st
import requests
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from pandas.io.json import json_normalize
import time as timee
import datetime
import calendar
import snelheidPlot


plotTab = st.sidebar.selectbox('Select Plot', ['___', 'Snelheid van een seizoen', '2'])

if plotTab == '___':
    st.title("Dashboard")
    st.header("Team Skating")
elif plotTab == 'Snelheid van een seizoen':
    st.title("Snelheid van een seizoen")
    snelheidPlot.runPlot()
elif plotTab == '2':
    st.title("2e plot")
else:
    st.error("Geen keuze gemaakt")
