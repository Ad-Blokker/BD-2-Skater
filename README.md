# Project Speed Skating Dashboard

This project is made for the speed skating coaches of KNSB (Royal Dutch Skaters Association).

## Get started

The project can be deployed inside a docker container by following these steps:

1. Clone the repository 

> git clone https://github.com/Ad-Blokker/BD-2-Skater.git

2. Within the main folder, run the following command to create a docker image:

> docker image build -t speedskating:app .

3. Start the container using the following command:

> docker run -p 80:8501 speedskating:app

Note: In this case port 80 is exposed by default (http). This can be changed to 443 (ssl) or any other port if necessary. Port 8501 is used internally for Streamlit

## Dashboard

The dashboard is made using the [Streamlit](https://www.streamlit.io/) library. It consist of a main file (/app/Dashboard.py) which initiates the other python files when a user selects a certain plot.

## About us


Team Skating

**Mark Blokker**  
500777384  
[mark.blokker@hva.nl](mailto:mark.blokker@hva.nl)  

**Talha Uçar**
500778614  
[talha.ucar@hva.nl](mailto:talha.ucar@hva.nl)

**Mellum Su**  
500776404  
[mellum.su@hva.nl](mailto:mellum.su@hva.nl)

**Sehit Karadağ**
500752424  
[sehit.karadag@hva.nl](mailto:sehit.karadag@hva.nl)

**Dax ten Voorde**
500804209  
[dax.ten.voorde@hva.nl](mailto:dax.ten.voorde@hva.nl)
