def runPlot():
        
    import streamlit as st
    import time as time
    import datetime
    import requests 
    import numpy
    import pandas as pd
    import numpy as np
    from pandas.io.json import json_normalize
    from PIL import Image


    SkaterLookupURL = "https://speedskatingresults.com/api/json/skater_lookup.php"
    PersonalRecordsURL =  "https://speedskatingresults.com/api/json/personal_records.php"


    #Ophalen van skaters a.d.h.v. achternaam
    def getSkaters(givenname,familyname):
        parameters = {'givenname':givenname,'familyname':familyname} 
        r = requests.get(url = SkaterLookupURL, params = parameters) 
        data = r.json() 
        results = json_normalize(data)
        resultsNormalized = pd.io.json.json_normalize(results.skaters[0])

        return resultsNormalized

    #Vinden van skater ID a.d.h.v. selectie in zijmenu
    def findSkaterID(chosenSkater, skatersFormatted,skaterListID):
        search = skatersFormatted.str.find(chosenSkater)
        listIndex = np.where(search == 0)
        skaterID = skaterListID[listIndex[0]]

        return int(skaterID)

    st.sidebar.header("Zoeken:") 
    givenname = st.sidebar.text_input('Voornaam')
    familyname = st.sidebar.text_input('Achternaam')

    #Schaatsers ophalen
    skatersList = getSkaters(givenname,familyname)
    skatersFormatted = skatersList['givenname']+ ' ' +  skatersList['familyname'] + ' (' +  skatersList['country'] + ')'
    skaterListID = skatersList['id']

    #Zijmenu: Dropdown met schaatsers
    chosenSkater = st.sidebar.selectbox('Schaatster',skatersFormatted)

    #Skater ID ophalen
    SkaterID = findSkaterID(chosenSkater,skatersFormatted,skaterListID)

    #st.sidebar.header("Filter:") 
    #distance = st.sidebar.radio("Afstand",(500, 1000, 1500, 3000, 5000, 10000))

    # Season Bests
    Parameters = {'skater':SkaterID} 

    r = requests.get(url = PersonalRecordsURL, params = Parameters) 

    data = r.json() 

    # Json to dataframe
    df = json_normalize(data)

    # Json column to new dataframe
    dfNormalized = pd.io.json.json_normalize(df.records[0])

    #lists
    st.title("Persoonlijke Records")

    if not dfNormalized.empty:
        distances = dfNormalized['distance'].values.tolist()

        times = dfNormalized['time'].values.tolist()

        # Info
        st.info("Schaatser: " + str(chosenSkater) + "   \nSkaterID: " + str(SkaterID))
        dfNormalized = dfNormalized.rename(columns={"date": "Datum", "distance": "Distance", "location": "Locatie","time": "Record tijd"})
        dfNormalized = dfNormalized[["Distance","Record tijd","Datum","Locatie"]]
        dfNormalized['Distance'] =  dfNormalized['Distance'].astype(str)+ "m"
        st.table(dfNormalized.set_index("Distance"))
        
    else: 
            st.header("Geen data") 











