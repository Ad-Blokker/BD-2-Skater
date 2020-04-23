
def runPlot():
    # Imports
    import streamlit as st
    import requests
    import pandas as pd
    import numpy as np
    from pandas.io.json import json_normalize
    import time as timee
    import datetime
    import calendar
    import snelheidPlot
    import plotly.express as px

    # Progress bar, status text, checking distance
    progress = 0
    progress_bar = st.sidebar.progress(progress)
    status_text = st.sidebar.empty()
    checkingDistance = st.sidebar.empty()

    # Zet skaterlookup url
    SkaterLookupURL = "https://speedskatingresults.com/api/json/skater_lookup.php"

    # Functie die skater ophaald voor de dropdown
    def getSkaters(givenname,familyname):
        parameters = {'givenname':givenname,'familyname':familyname} 
        r = requests.get(url = SkaterLookupURL, params = parameters) 
        data = r.json() 
        results = json_normalize(data)
        resultsNormalized = pd.io.json.json_normalize(results.skaters[0])

        return resultsNormalized

    # Functie die skaterID vindt
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


    # URL
    URL = "https://speedskatingresults.com/api/json/skater_results.php"
    
    
    # list die gevuld gaat worden met distances waarbij geen data is
    emptydistances = []

    # list van alle distances
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

    # Info
    st.header("Info:")
    st.info("Schaatser: " + str(chosenSkater) + "   \nSkaterID: " + str(SkaterID))
    
    # For loop zodat elke distance gecheckt wordt
    for distance in distances:
        Distance = distance
             
        # Set checking distance
        checkingDistance.text("Checking Afstand: %im " % distance)

        # Api resultaat ophalen
        Parameters = {'skater': SkaterID, 'distance': Distance}
        r = requests.get(url=URL, params=Parameters)
        data = r.json()

        # Json to dataframe
        df = json_normalize(data)

        # Json column to new dataframe
        dfCompetitions = pd.io.json.json_normalize(df.results[0])

        # Check of dataframe is leeg
        # Else niet plotten
        if not dfCompetitions.empty and not len(dfCompetitions.index) == 1:
            dfCompetitions.drop(columns=['link'])

            for index, row in dfCompetitions.iterrows():
                if '.' in dfCompetitions['time'].iloc[index]:
                    x = timee.strptime(
                        dfCompetitions['time'].iloc[index].split(',')[0], '%M.%S')

                    dfCompetitions['time'].iloc[index] = datetime.timedelta(
                        minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
                else:
                    dfCompetitions['time'].iloc[index] = dfCompetitions['time'].iloc[index].replace(
                        ',', '.')
            # Convert naar int
            dfCompetitions['time'] = pd.to_numeric(dfCompetitions['time'])

            # Nieuwe empty list om een nieuwe dataframe te maken
            data = []
            
            dfCompetitions['date'] = pd.to_datetime(dfCompetitions['date'])

            dfCompetitions = dfCompetitions.sort_values(by='date')

            # Set figure
            fig = px.line(dfCompetitions, x="date", y="time")

            # Update figure layout
            fig.update_layout(
                title='Plot Afstanden op Locatie ' + str(Distance) + 'm',
                xaxis_title="Datum",
                yaxis_title="Tijd (s)",
                height=400,\
            )

            # Plotly chart
            st.plotly_chart(fig, use_container_width=True)


            # Print lange doorgetrokken lijn om afstanden makkelijker te zien splitsen
            slashes = '-' * 30
            st.write(slashes)


        else:
            # Vul emptydistances list met de empty distance
            emptydistances.append(distance)

            # Als emptydistances alle distances bevat geef melding
            if emptydistances == distances:
                st.error("GEEN DATA     \n Voeg data toe voor " + str(chosenSkater) +
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