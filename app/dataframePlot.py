
def runPlot():
    import streamlit as st
    import numpy as np
    import requests 
    import pandas as pd
    from pandas.io.json import json_normalize

    # Progress bar, status text, checking distance
    progress = 0
    progress_bar = st.sidebar.progress(progress)
    status_text = st.sidebar.empty()
    checkingDistance = st.sidebar.empty()


    SkaterLookupURL = "https://speedskatingresults.com/api/json/skater_lookup.php"
    URL =  "https://speedskatingresults.com/api/json/skater_results.php"


    #Retrieving skaters by firstname and lastname
    def getSkaters(givenname,familyname):
        parameters = {'givenname':givenname,'familyname':familyname} 
        r = requests.get(url = SkaterLookupURL, params = parameters) 
        data = r.json() 
        results = json_normalize(data)
        resultsNormalized = pd.io.json.json_normalize(results.skaters[0])

        return resultsNormalized

    #Retrieving Skater ID of the chosen skater (in the side menu)
    def findSkaterID(chosenSkater, skatersFormatted,skaterListID):
        search = skatersFormatted.str.find(chosenSkater)
        listIndex = np.where(search == 0)
        skaterID = skaterListID[listIndex[0]]

        return int(skaterID)


    #List of distances
    distances = [100,
        200,
        300,
        400,
        500,
        700,
        1000,
        1500,
        3000,
        5000,
        10000]
    
    # Sidebar inputs for skaters
    st.sidebar.header("Zoeken:") 
    givenname = st.sidebar.text_input('Voornaam')
    familyname = st.sidebar.text_input('Achternaam')
    
    #Retrieving skaters with user input
    try: 
        skatersList = getSkaters(givenname,familyname)
        skatersFormatted = skatersList['givenname']+ ' ' +  skatersList['familyname'] + ' (' +  skatersList['country'] + ')'
        skaterListID = skatersList['id']
    except:
        st.error("Geen schaatser met deze naam gevonden")

    #Sidebar dropdown menu with a list of skaters (results of search query)
    chosenSkater = st.sidebar.selectbox('Schaatster',skatersFormatted)

    #Getting Skater ID of chosen skater
    SkaterID = findSkaterID(chosenSkater,skatersFormatted,skaterListID)

    emptydistances = []

    for distance in distances:
        Distance = distance
                     
        # Set checking distance
        checkingDistance.text("Checking Afstand: %im " % distance)

        # Retrieving data using API
        Parameters = {'skater': SkaterID, 'distance': Distance}
        r = requests.get(url=URL, params=Parameters)
        data = r.json()

        # Json to dataframe
        df = json_normalize(data)

        # Json column to new dataframe
        dfCompetitions = pd.io.json.json_normalize(df.results[0])
    
        if not dfCompetitions.empty:
            # if st.checkbox('Is een hamer neutraal?'):
            st.write(str(Distance) +'m:')

            # drop link column
            dfCompetitions = dfCompetitions.drop(columns=['link'])

            dfCompetitions = dfCompetitions.rename(columns={"time": "Gereden tijd", "date": "Datum", "name": "Toernooi","location": "Locatie"})
            # dfCompetitions = dfCompetitions[["Distance","Record time","Date","Location"]]

            st.write(dfCompetitions)
        else:
            emptydistances.append(distance)            
            # If empty distances contain all distances
            if emptydistances == distances:
                st.error("Geen data     \n Voeg data toe voor " + str(chosenSkater) +
                        " op speedskatingresults.com om hier een grafiek te plotten")
        # Set progressbar
        if progress == 90:
            progress = 100
        else:
            progress += 9
        progress_bar.progress(progress)
        status_text.text("%i%% Compleet" % progress)

        # Set checking distance
        if distance == 10000:
            checkingDistance.empty()
