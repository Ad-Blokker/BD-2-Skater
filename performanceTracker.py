
def runPlot():
    # Imports
    import streamlit as st
    import requests
    import pandas as pd
    import numpy as np
    from pandas.io.json import json_normalize
    import time as time
    import datetime
    import calendar
    import snelheidPlot
    import plotly.graph_objects as go
    from datetime import datetime as dt

    # Zet skaterlookup url
    SkaterLookupURL = "https://speedskatingresults.com/api/json/skater_lookup.php"

    # Functie die skater ophaald voor de dropdown
    def getSkaters(givenname,familyname):
        parameters = {'givenname':givenname,'familyname':familyname} 
        r = requests.get(url = SkaterLookupURL, params = parameters) 
        data = r.json() 
        results = json_normalize(data)
        resultsNormalized = pd.json_normalize(results.skaters[0])

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

    # Info
    st.header("Info:")
    st.info("Schaatser: " + str(chosenSkater) + "   \nSkaterID: " + str(SkaterID))

    # SkaterID = 23493
    start = 2007
    end = 2020
    Distance = 1500

    # SBT resultaat ophalen
    def getSBT(SkaterID,start,end,Distance):
        Parameters = {'skater': SkaterID, 'start': start, 'end': end, 'distance': Distance}
        # URL
        URL = "https://speedskatingresults.com/api/json/season_bests.php"
        r = requests.get(url = URL, params = Parameters) 
        data = r.json() 
        results = json_normalize(data)
        resultsNormalized = pd.json_normalize(results.seasons[0])

        return resultsNormalized

    # SBT resultaat ophalen
    def getWorldRecord(Gender, Age, Distance):
        Parameters = {'gender': Gender, 'age': Age, 'distance': Distance}
        # URL
        URL = "https://speedskatingresults.com/api/json/world_records.php"
        r = requests.get(url = URL, params = Parameters) 
        data = r.json() 
        results = json_normalize(data)
        resultsNormalized = pd.json_normalize(results.records[0])

        return resultsNormalized
    
    # Gender input
    Gender = 'm'

    GenderOption = st.sidebar.radio("Gender", ('Man', 'Vrouw'))

    if GenderOption == 'Man':
        Gender = 'm'
    elif GenderOption == 'Vrouw':
        Gender = 'f'
    else:
        st.write("Geen optie geselecteerd")

    # Leeftijdscategorie input
    ageCate = 'jr'

    ageCat = st.sidebar.radio("Leeftijdscategorie", ('Junior', 'Senior'))

    if ageCat == 'Junior':
        ageCate = 'jr'
    elif ageCat == 'Senior':
        ageCate = 'sr'
    else:
        st.write("Geen optie geselecteerd")

    # dataframe ophalen uit defWorldRecords
    dfWorldRecord = getWorldRecord(Gender, ageCate, 1500)
    dfWorldRecord['name'] = dfWorldRecord[['skater.givenname', 'skater.familyname']].apply(lambda x: ' '.join(x), axis=1)
    dfWorldRecord = dfWorldRecord.rename(columns={'gender': 'Gender', 'age': 'Leeftijds Categorie', 'distance': 'Afstand', 'time': 'Gereden tijd', 'name': 'Behaald door'})

    st.subheader('Wereld Record:')
    st.write(dfWorldRecord[['Gender', 'Leeftijds Categorie', 'Afstand', 'Gereden tijd', 'Behaald door']])

    # dfSBT_nor1 zijn alle results met de jaren los
    dfSBT_nor1 = getSBT(SkaterID,start,end,Distance)
    
    # checkt of er genoeg data is
    if not dfSBT_nor1.empty and not len(dfSBT_nor1.index) <= 2:

        # Nieuwe lijst zodat er een dataframe gevuld kan worden
        dataSBT = []
        dataWR = []

        # Tijdelijke dataframe die gebruikt wordt om later een dataframe te maken
        temp = pd.DataFrame(columns=['distance', 'time', 'date', 'location'])

        # Record met alle info
        difference = end - start - 1
        
        # World record
        WR = dfWorldRecord['Gereden tijd'].iloc[0]

        # For loop op de API result naar een nieuwe dataframe te krijgen
        for i in range(difference):
            try: 
                temp = pd.json_normalize(dfSBT_nor1.records[i])
                jaar = dfSBT_nor1['start'].iloc[i]
                afstand = temp['distance'].iloc[0]

                tijd = temp['time'].iloc[0]

                datum = temp['date'].iloc[0]
                location = temp['location'].iloc[0]

                WR = dfWorldRecord['Gereden tijd'].iloc[0]

                dataWR.append([datum, WR])

                dataSBT.append([jaar, afstand, tijd, datum, location])
            except:
                print('stop')

        # Vult de nieuwe SBT dataframe met de gegevens die hierboven gekregen zijn
        dfSBT = pd.DataFrame(data=dataSBT, columns=['season_year','distance', 'time', 'date', 'location'])

        # Vult de nieuwe WR dataframe met de gegevens die hierboven gekregen zijn
        dfWorldRecordDataframe = pd.DataFrame(data=dataWR, columns=['date','time'])
        
        # Print de dataframe uit
        st.subheader('Season bests van ' + str(chosenSkater) + ':')
        st.write(dfSBT)
                
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dfSBT['date'], y=dfSBT['time'],
                    mode='lines',
                    name=str(chosenSkater)))

        fig.add_trace(go.Scatter(x=dfWorldRecordDataframe['date'], y=dfWorldRecordDataframe['time'],
            mode='lines',
            name='WR'
        ))


        # Update figure layout
        fig.update_layout(
            title='Snelheid van ' + str(Distance) + 'm',
            xaxis_title="Datum",
            yaxis_title="Tijd",
        )

        # Plotly chart
        st.plotly_chart(fig, use_container_width=True)


    else:
        st.error("GEEN DATA     \n Voeg data toe voor " + str(chosenSkater) + " op speedskatingresults.com om hier een grafiek te plotten")
