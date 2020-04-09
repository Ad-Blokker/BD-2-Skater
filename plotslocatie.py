def runPlot():

    import streamlit as st
    import time as time
    import datetime
    import requests 
    import numpy
    import pandas as pd
    import plotly.graph_objs as go
    import numpy as np
    from pandas.io.json import json_normalize
    from bokeh.plotting import figure
    import altair as alt
    import time as timee




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
    skatersList = getSkaters(givenname,familyname)
    skatersFormatted = skatersList['givenname']+ ' ' +  skatersList['familyname'] + ' (' +  skatersList['country'] + ')'
    skaterListID = skatersList['id']

    #Zijmenu: Dropdown met schaatsers
    chosenSkater = st.sidebar.selectbox('Schaatster',skatersFormatted)

    #Skater ID ophalen
    SkaterID = findSkaterID(chosenSkater,skatersFormatted,skaterListID)

    #st.sidebar.header("Filter:") 
    #distance = st.sidebar.radio("Afstand",(500, 1000, 1500, 3000, 5000, 10000))

    # URL
    URL = "https://speedskatingresults.com/api/json/skater_results.php"

    Parameters = {'skater': SkaterID}
    r = requests.get(url=URL, params=Parameters)
    data = r.json()

    # Json to dataframe
    df = json_normalize(data)

    # Json column to new dataframe
    dfNormalized = pd.io.json.json_normalize(df.results[0])

    dfLocation = dfNormalized.groupby('location', axis='columns')

    # # Season Bests
    # Parameters = {'skater':SkaterID} 

    # r = requests.get(url = PersonalRecordsURL, params = Parameters) 

    # data = r.json() 

    # # Json to dataframe
    # df = json_normalize(data)

    # # Json column to new dataframe
    # dfNormalized = pd.io.json.json_normalize(df.records[0])

    #lists
    st.title("Plots with location")

    if not dfNormalized.empty:
        dates = dfNormalized['date'].values.tolist()


        for index, row in dfNormalized.iterrows():
            if '.' in dfNormalized['time'].iloc[index]:
                x = timee.strptime(
                    dfNormalized['time'].iloc[index].split(',')[0], '%M.%S')

                dfNormalized['time'].iloc[index] = datetime.timedelta(
                    minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            else:
                dfNormalized['time'].iloc[index] = dfNormalized['time'].iloc[index].replace(
                    ',', '.')
        # Convert naar int
        dfNormalized['time'] = pd.to_numeric(dfNormalized['time'])


        data = []

        # Bereken snelheid en zet in list
        for index, row in dfNormalized.iterrows():
            strindex = str(index + 1)

            # Tijd variable uit de kollom halen
            time = dfNormalized['time'].iloc[index]

            # Data list met gegevens geven
            data.append([strindex, time])

        # Set list to dataframe
        cols = ['id', 'time']
        dfTimes = pd.DataFrame(data, columns=cols)


        times = dfNormalized['time'].values.tolist()
        
        location = dfNormalized['location'].values.tolist()
        locations = str(location)[1:-1]

        st.header("Info:") 
        st.write("Naam: " + str(chosenSkater) + "   \nSkaterID: " + str(SkaterID))
        st.dataframe(dfNormalized)

        dfNormalized.set_index('date')

        st.header("Chart:") 

        chart = dfNormalized.set_index('date')

        chart_data = pd.DataFrame(
            np.random.randn(15, 7),
            columns=['Heerenveen (NED)','Kolomna (RUS)','Calgary (CAN)','Berlin (GER)','Inzell (GER)','Hamar (NOR)','Amsterdam-Olympic (NED)'
        ])

        st.line_chart(chart_data)

    else: 
            st.header("Geen data") 