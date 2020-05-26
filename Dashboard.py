# Imports
import streamlit as st
import snelheidPlot
import dataframePlot
import personal_records
import plotslocatie
import performanceTracker
import plotMetTijden
import home
from PIL import Image

html = """
<style>
.sidebar .sidebar-content {
  background-color: #F39D12;
  background-image: none;
  color: white;
}

.sidebar img{
    margin-top: -35px;  
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
.stMultiSelect label{
    color:white;
}
.logo{
    width:250px;
}
.knsb{
    width:100px;
    position:fixed;
    bottom:3px;
    padding-bottom:10px;
    right:20px;
    z-index:5;
}
.hva{
    width:135px;
    position:fixed;
    bottom:-17px;
    right:130px;
    z-index:5;
}
.datavalley{
    width:100px;
    position:fixed;
    bottom:10px;
    right:280px;
    z-index:5;
}
.sidebar{
    z-index:10;
}

</style>
"""
speedskatinglogo = "<img class=\"logo\" src=\"https://i.imgur.com/aF1Lgnx.png\" />"
logos = """

<img class="knsb" src=\"https://i.imgur.com/VSveX8J.png\" /> 
<img class="hva" src=\"https://i.imgur.com/JMyruEu.png\" /> 
<img class="datavalley" src=\"https://i.imgur.com/gysnqiq.png\" /> 

"""


st.markdown(html, unsafe_allow_html=True)
st.sidebar.markdown(speedskatinglogo, unsafe_allow_html=True)

# Dropdown met de keuze qua plots
plots = ['Home', 'Performance Tracker', 'Gemiddelde snelheid', 'Persoonlijke Records','Locatie plot', 'Plots met tijden', 'Alle Data']
plotTab = st.sidebar.selectbox('Selecteer een Plot', plots)

st.markdown(logos, unsafe_allow_html=True)


# If en elif's die scripts oproepen om de plots te maken
if plotTab == 'Home': #default
    home.runPlot()
    # st.title("Dashboard")
    # st.header("Team Skating")
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
elif plotTab == 'Plots met tijden': #plotMetTijden
    plotMetTijden.runPlot()
else: #Foutmelding
    st.error("Geen keuze gemaakt in het menu")
