# Imports
import streamlit as st
import snelheidPlot
import dataframePlot
import personal_records
import plotslocatie
import performanceTracker
from PIL import Image

html = """
<style>
.sidebar .sidebar-content {
  background-color: #F39D12;
  background-image: none;
  color: white;
}

.image-container img{
    margin-top: -35px
}

.stTextInput label{
    color:white;
}
.stSelectbox label{
    color:white;
}

.stRadio label{
    color:white;
}


</style>
"""

st.markdown(html, unsafe_allow_html=True)

image = Image.open('logo.png')
st.sidebar.image(image, width= 250,)

# Dropdown met de keuze qua plots
plots = [' ', 'Performance Tracker', 'Gemiddelde snelheid', 'Persoonlijke Records','Locatie plot', 'Alle Data']
plotTab = st.sidebar.selectbox('Selecteer een Plot', plots)

# If en elif's die scripts oproepen om de plots te maken
if plotTab == ' ': #default
    st.title("Dashboard")
    st.header("Team Skating")
elif plotTab == 'Performance Tracker': #performanceTracker
    st.title('Performance tracker')
    performanceTracker.runPlot()
elif plotTab == 'Gemiddelde snelheid': #snelheidPlot
    st.title("Gemiddelde snelheid van alle seizoenen")
    snelheidPlot.runPlot()
elif plotTab == 'Persoonlijke Records': #personal_records
    personal_records.runPlot()
elif plotTab == 'Locatie plot': #plotslocatie
    plotslocatie.runPlot()
elif plotTab == 'Alle Data': #dataframePlot
    dataframePlot.runPlot()
else: #Foutmelding
    st.error("Geen keuze gemaakt in het menu")
