# Imports
import streamlit as st
import snelheidPlot
import personal_records

# Dropdown met de keuze qua plots
plotTab = st.sidebar.selectbox('Selecteer een Plot', ['___', 'Snelheid van een seizoen', 'Persoonlijke Records'])

# If en elif's die scripts oproepen om de plots te maken
if plotTab == '___': #default
    st.title("Dashboard")
    st.header("Team Skating")
elif plotTab == 'Snelheid van een seizoen': #snelheidPlot
    st.title("Snelheid van een seizoen")
    snelheidPlot.runPlot()
elif plotTab == 'Persoonlijke Records': #personal_records
    personal_records.runPlot()
else: #Foutmelding
    st.error("Geen keuze gemaakt in het menu")
