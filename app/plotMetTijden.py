
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

    # API source
    SkaterLookupURL = "https://speedskatingresults.com/api/json/skater_lookup.php"

    # Retrieving skaters by firstname and lastname
    def getSkaters(givenname,familyname):
        parameters = {'givenname':givenname,'familyname':familyname} 
        r = requests.get(url = SkaterLookupURL, params = parameters) 
        data = r.json() 
        results = json_normalize(data)
        resultsNormalized = pd.io.json.json_normalize(results.skaters[0])

        return resultsNormalized

    # Retrieving Skater ID of the chosen skater (in the side menu)
    def findSkaterID(chosenSkater, skatersFormatted,skaterListID):
        search = skatersFormatted.str.find(chosenSkater)
        listIndex = np.where(search == 0)
        skaterID = skaterListID[listIndex[0]]

        return int(skaterID)

    # Sidebar inputs for skaters
    st.sidebar.header("Zoeken:") 
    givenname = st.sidebar.text_input('Voornaam')
    familyname = st.sidebar.text_input('Achternaam')

    # Retrieving skaters with user input
    skaterDoesntExist = False
    try: 
        skatersList = getSkaters(givenname,familyname)
        skatersFormatted = skatersList['givenname']+ ' ' +  skatersList['familyname'] + ' (' +  skatersList['country'] + ')'
        skaterListID = skatersList['id']
    except:
        skaterDoesntExist = True

  
    #Error if skater the user searched for does not exist
    if skaterDoesntExist == True:
        st.warning("Fout: Deze schaatscher is niet gevonden op speedskatingresults.com")

    else:

        # Sidebar dropdown menu with a list of skaters (results of search query)
        chosenSkater = st.sidebar.selectbox('Schaatster',skatersFormatted)

        # Getting Skater ID of chosen 
        SkaterID = findSkaterID(chosenSkater,skatersFormatted,skaterListID)


        # URL
        URL = "https://speedskatingresults.com/api/json/skater_results.php"
        
        
        # list that will be filled with distances where there are no data
        emptydistances = []

        # List with all the distances
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
        st.info("Schaatser: " + str(chosenSkater) + "   \nSkaterID: " + str(SkaterID))

        selectedDistances = []

        selectedDistances = st.sidebar.multiselect('afstanden', distances)

        checkAllDistance = st.sidebar.checkbox('Alle afstanden')

        if checkAllDistance:
            selectedDistances = distances

        if not selectedDistances:
            st.warning('Geen afstanden geselecteerd')
        else:
            selectedDistances = sorted(selectedDistances)
            
        # For loop to check all the distances
        for distance in selectedDistances:
            Distance = distance

            # Get API results
            Parameters = {'skater': SkaterID, 'distance': Distance}
            r = requests.get(url=URL, params=Parameters)
            data = r.json()

            # Json to dataframe
            df = json_normalize(data)

            # Json column to new dataframe
            dfCompetitions = pd.io.json.json_normalize(df.results[0])

            # Check if the dataframe is empty
            # Else Do not plot
            if not dfCompetitions.empty and not len(dfCompetitions.index) == 1:
                dfCompetitions.drop(columns=['link'])
                dfCompetitions = dfCompetitions.rename({"name": "Event"}, axis="columns")

                for index, row in dfCompetitions.iterrows():
                    if '.' in dfCompetitions['time'].iloc[index]:
                        x = timee.strptime(
                            dfCompetitions['time'].iloc[index].split(',')[0], '%M.%S')

                        dfCompetitions['time'].iloc[index] = datetime.timedelta(
                            minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
                    else:
                        dfCompetitions['time'].iloc[index] = dfCompetitions['time'].iloc[index].replace(
                            ',', '.')
                # Convert to int
                dfCompetitions['time'] = pd.to_numeric(dfCompetitions['time'])

                # New empty list to create a new dataframe
                data = []
                
                dfCompetitions['date'] = pd.to_datetime(dfCompetitions['date'])

                dfCompetitions = dfCompetitions.sort_values(by='Event')

                # Set figure
                fig = px.scatter(dfCompetitions, x="date", y="time", color='Event')


                # Update figure layout
                fig.update_layout(
                    #title='Plot Afstanden op Locatie ' + str(Distance) + 'm',
                    xaxis_title="Datum",
                    yaxis_title="Tijd (s)",
                    height=400,\
                )
                dfCompetitions = dfCompetitions.sort_values(by='date')
                dfTrend = dfCompetitions['time'].copy()
                dfTrend = dfTrend.reset_index(drop=True)

                fig2 = px.scatter(dfTrend, x=dfTrend.index, y=dfCompetitions['time'], trendline='ols', trendline_color_override='red', marginal_y="violin")

                fig2.update_layout(
                    #title='Trend van ' + str(Distance) + 'm',
                    xaxis_title="Keren gereden",
                    yaxis_title="tijd (s)",
                )

                # Plotly chart
                st.subheader('Plot afstanden op locatie ' + str(Distance) + 'm')
                st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(fig2, use_container_width=True)


            else:
                # Fill emptydistances list with the empty distance
                emptydistances.append(distance)
                if not distances == selectedDistances: 
                    st.warning('Er is geen data gevonden voor ' + str(chosenSkater) + ' op de ' + str(Distance) + 'm.')

                # If empty distances all distances contains no notification
                if emptydistances == distances:
                    st.error("GEEN DATA     \n Voeg data toe voor " + str(chosenSkater) +
                            " op speedskatingresults.com om hier een grafiek te plotten")
