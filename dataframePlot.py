
def runPlot():

    import streamlit as st
    import numpy as np
    import requests 
    import pandas as pd
    from pandas.io.json import json_normalize


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


    # Zijmenu: Achternaam zoeken
    st.sidebar.header("Zoeken:") 
    givenname = st.sidebar.text_input('Voornaam')
    familyname = st.sidebar.text_input('Achternaam')
    
    #Schaatsers ophalen
    try: 
        skatersList = getSkaters(givenname,familyname)
        skatersFormatted = skatersList['givenname']+ ' ' +  skatersList['familyname'] + ' (' +  skatersList['country'] + ')'
        skaterListID = skatersList['id']
    except:
        st.error("---GEEN SCHAATSER MET DEZE NAAM GEVONDEN---")

    #Zijmenu: Dropdown met schaatsers
    chosenSkater = st.sidebar.selectbox('Schaatster',skatersFormatted)

    #Skater ID ophalen
    SkaterID = findSkaterID(chosenSkater,skatersFormatted,skaterListID)

    # Competition list
    URL =  "https://speedskatingresults.com/api/json/skater_competitions.php"

    Season = 2012

    Parameters = {'skater':SkaterID, 'season' : Season} 

    r = requests.get(url = URL, params = Parameters) 

    data = r.json()

    # Json to dataframe
    from pandas.io.json import json_normalize
    df = json_normalize(data)

    # Json column to new dataframe
    dfCompetitions = pd.io.json.json_normalize(df.competitions[0])

    if not dfCompetitions.empty:
        # if st.checkbox('Is een hamer neutraal?'):
        st.subheader('Data:')

        # drop link column
        dfCompetitions = dfCompetitions.drop(columns=['link', 'id', 'trackid'])

        dfCompetitions = dfCompetitions.rename(columns={"name": "Event", "startdate": "Start Datum", "enddate": "Eind datum","location": "Locatie"})
        # dfCompetitions = dfCompetitions[["Distance","Record time","Date","Location"]]

        st.write(dfCompetitions)
    else:
        st.error('Geen data van deze persoon gevonden')