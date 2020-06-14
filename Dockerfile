FROM python:3

# streamlit-specific commands
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

#Openen van port 8501
EXPOSE 8501

#Lijst van requirements naar container kopieren en installeren
ADD ./app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#De hele app naar de container kopieren
ADD ./app /opt/webapp/

WORKDIR /opt/webapp

#Streamlit starten
CMD streamlit run Dashboard.py
