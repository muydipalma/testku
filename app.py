import streamlit as st
import pandas as pd 
import plotly_express as px 
import folium 
from folium.plugins import HeatMap
import seaborn as sns
import requests
import time
import json

# Get the data from url and request it as json file
@st.cache(persist=True, suppress_st_warning=True)
def load_data():
    urlp0='https://www.pami.org.ar/centros-vacunacion'
    dataf = {'provincia':'BUENOS AIRES', 'localidad':'AVELLANEDA'}
    r_p0 = requests.post(urlp0, dataf)
    df=pd.DataFrame.from_dict(r_p0.json())
    url = 'http://photon.komoot.de/api/?q='
    for x in df.iterrows():
        address=x[1]['domicilio']+' '+ x[1]['localidad']
        resp = requests.get(url=url+address)
        data = json.loads(resp.text)
        try:
            print (data['features'][0]['geometry']['coordinates'])
            x[1]['latitud']=data['features'][0]['geometry']['coordinates'][0]
            x[1]['longitud']=data['features'][0]['geometry']['coordinates'][1]
        except:
            print('not found')
        time.sleep(0.5)
    df.dropna(subset=['latitud', 'longitud'],inplace=True)
      
    return df

@st.cache(persist=True, suppress_st_warning=True)
def display_map(df):
    st.subheader(" Displaying Point based map")
    px.set_mapbox_access_token(
        "pk.eyJ1Ijoic2hha2Fzb20iLCJhIjoiY2plMWg1NGFpMXZ5NjJxbjhlM2ttN3AwbiJ9.RtGYHmreKiyBfHuElgYq_w")
    fig = px.scatter_mapbox(df, lat='longitud', lon='latitud', zoom=10)
    return fig

    
def main():
    df_data = load_data()
    #st.header('Campaña vacunacion 2020')
    #st.subheader('farmacias habilitadas')
    #st.image('image.png', width=600)
    if st.checkbox('Show'):
        st.write(df_data.head())
        st.write(df_data.shape)
    st.plotly_chart(display_map(df_data))
if __name__ == '__main__':
    main()
