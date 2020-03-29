
# Imports
import streamlit as st
import requests 
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from pandas.io.json import json_normalize
import time as timee
import datetime, calendar

# Schaatsers data naar pandas dataframe
skatersid = [831, 31536, 687, 5487, 5796, 6588]
skatersfullname = ['Sven Kramer', 'Jutta Leerdam', 'Ireen Wüst', 'Kjeld Nuis', 'Lotte van Beek', 'Kai Verbij']
dfSchaatsers = pd.DataFrame(list(zip(skatersid, skatersfullname)),columns=['Skater_id', 'Skater_fullname'])

# Progress bar, status text, checking distance
progress = 0
progress_bar = st.sidebar.progress(progress)
status_text = st.sidebar.empty()
checkingDistance = st.sidebar.empty()

# Set pagina title
st.title("Snelheid van een seizoen")

# User input naam en seizoen
Skatername = st.sidebar.selectbox("Schaatser", dfSchaatsers['Skater_fullname'].tolist())
Season = st.sidebar.slider("Seizoen", 2007,2020)

# Checkt of er knop wordt ingedrukt
if st.sidebar.button("Laat grafiek zien"):
    # Schaatser naam naar id
    idschaatser = dfSchaatsers.loc[dfSchaatsers['Skater_fullname'] == Skatername]
    idschaatser = idschaatser.reset_index(drop=True)
    idschaatser = idschaatser.loc[0].at['Skater_id']
    SkaterID = idschaatser

    # Info
    st.header("Info:") 
    st.info("Schaatser: " + str(Skatername) + "   \nSkaterID: " + str(SkaterID) + "   \nSeizoen: " + str(Season))

    # Ipv aantal runs datum maar dit werkt nog niet
    # def add_months(sourcedate,months):
    #     month = sourcedate.month - 1 + months
    #     year = sourcedate.year + month / 12
    #     month = month % 12 + 1
    #     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    #     return datetime.date(year,month,day)

    # Api
    URL =  "https://speedskatingresults.com/api/json/skater_results.php"

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

    # For loop zodat elke distance gecheckt wordt
    for distance in distances:
        Distance = distance

        # Api resultaat ophalen
        Parameters = {'skater':SkaterID, 'distance':Distance, 'season': Season} 
        r = requests.get(url = URL, params = Parameters) 
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
                    x = timee.strptime(dfCompetitions['time'].iloc[index].split(',')[0],'%M.%S')

                    dfCompetitions['time'].iloc[index] = datetime.timedelta(minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
                else:
                    dfCompetitions['time'].iloc[index] = dfCompetitions['time'].iloc[index].replace(',','.')
            # to numeric
            dfCompetitions['time'] = pd.to_numeric(dfCompetitions['time'])

            # Create empty list om een nieuwe dataframe te maken
            data = []

            # Calc speed and set in list
            for index, row in dfCompetitions.iterrows():
                strindex = str(index + 1)

                # Tijd variable uit de kollom halen
                time = dfCompetitions['time'].iloc[index]

                # Datum
                # date = dfCompetitions['date'].iloc[index]
                # date = add_months(datetime.datetime(*[int(item) for item in date.split('-')]), 1).strftime("%Y-%m-%d")

                # Snelheid variable berekenen naar km/h
                speedEach = (Distance / time) * 3.6

                # Data list met gegevens geven
                data.append([strindex, speedEach])
                
            # Set list to dataframe
            cols = ['id', 'speed']
            dfSpeed = pd.DataFrame(data, columns=cols)

            # Set figure en plot het
            fig = figure(
                title = 'Snelheid van ' +str(Distance) + "m",
                x_axis_label='Aantal runs',
                y_axis_label='Snelheid in km/h'
            )
            fig.plot_height =  400
            fig.line(dfSpeed['id'], dfSpeed['speed'], legend='Snelheid', line_width=2)

            # Set sort chart
            st.bokeh_chart(fig, use_container_width=True)

        else:
            # Vul emptydistances list met de empty distance
            emptydistances.append(distance)

            #Print Distance in console    
            print("Distance: " + str(Distance) + " is empty.")

            # Als emptydistances alle distances bevat geef melding
            if emptydistances == distances:
                st.error("GEEN DATA     \n Voeg data toe aan speedskatingresults.com om hier een grafiek te plotten")
        
        # Set progressbar  
        if progress == 90:
            progress = 100
        else:
            progress += 9
        progress_bar.progress(progress)
        status_text.text("%i%% Compleet" % progress)

        # Set checking distance
        if distance == 10000:
            checkingDistance.text("Alle afstanden gecheckt")
        else: 
            checkingDistance.text("Checking Afstand: %im " % distance)


