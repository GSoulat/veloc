from flask import Blueprint, render_template
import requests
import pandas as pd
import time
import numpy as np
import pickle
import plotly
import plotly.express as px
import json
from lightgbm import LGBMRegressor
from dotenv import load_dotenv
import os
load_dotenv()

home = Blueprint("home", __name__, static_folder="../static", template_folder="../templates/")

openmodel = open("App/routes/model_rf.pkl", "rb")

model = pickle.load(openmodel)

list_weather1 = ['clear sky', 'few clouds']
list_weather2 = ['mist', 'Smoke', 'Haze', 'Thursday', 'sand/ dust whirls', 'fog', 'light intensity drizzle','drizzle','light intensity drizzle rain',
                    'drizzle rain','shower rain and drizzle','shower drizzle','broken clouds']
list_weather3 = ['light rain', 'moderate rain', 'light snow', 'Snow', '	Sleet','Light shower sleet','Shower sleet','Light rain and snow','Light rain and snow',
                    'Light shower snow', 'Shower snow', 'sand','dust','heavy intensity drizzle','heavy intensity drizzle rain','heavy shower rain and drizzle',
                    'overcast clouds', 'scattered clouds']
list_weather4 = ['thunderstorm with light rain', 'thunderstorm with rain', 'thunderstorm with heavy rain', 'light thunderstorm', 'thunderstorm',
                    'heavy thunderstorm','	ragged thunderstorm','thunderstorm with light drizzle','thunderstorm with drizzle','thunderstorm with heavy drizzle',
                    'heavy intensity rain','very heavy rain','extreme rain','freezing rain','light intensity shower rain','shower rain',
                    'heavy intensity shower rain', 'ragged shower rain', 'Heavy snow', 'Heavy shower snow', 'volcanic ash', 'squalls','tornado']

@home.route('/')
@home.route('/home')
def home_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    
    return render_template('home.html')  

@home.route('/journalier')
def journalier_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """

    api_key = os.getenv('api_key_open_weather')
    lat = "38.89438"
    lon = "-77.03160"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url).json()
    prediction = []
    temp_day = 0
    api_key_holiday= os.getenv('api_key_holiday')
    
    df_data48h = pd.DataFrame(data=response['hourly'])
    df_data48h = df_data48h.drop(["pressure","dew_point", "uvi", "clouds", "visibility", "wind_deg", "wind_gust", "pop"], axis=1)
    for data48h in response['hourly']:
        date = time.strftime("%D", time.localtime(int(data48h['dt'])))
        hours = time.strftime("%H", time.localtime(int(data48h['dt'])))
        temp = data48h['temp']
        humidity = data48h['humidity']
        windspeed = data48h['wind_speed']
        month = time.strftime("%m", time.localtime(int(data48h['dt'])))
        date = pd.to_datetime(date)
        year = date.year
        weekday = date.weekday()
        day = date.day
        climat = data48h['weather'][0]['description']
        # print(climat)
        
        if climat in list_weather1:
            weather = 1
        elif climat in list_weather2:
            weather = 2
        elif climat in list_weather3:
            weather = 3
        else:
            weather = 4
        # print(weather)
        if day != temp_day:
            url_holiday = "https://holidays.abstractapi.com/v1/?api_key=%s&country=US&year=%s&month=%s&day=%s" % (api_key_holiday, year, month ,day)
            response_holiday = requests.get(url_holiday).json()
            temp_day = day

        list_working = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            
        if response_holiday =='':
            holiday = 0
            if weekday in list_working:
                workingday = 1
            else:
                workingday = 0
        else:
            holiday = 1
            workingday = 0
            

        features = [holiday, workingday, weather, temp, humidity, windspeed, month, hours,weekday,year]
        final_features = [np.array(features)]
        df = pd.DataFrame()
        df[['holiday','workingday','weather','temp','humidity','windspeed','month','hours','weekday','year']] = final_features
        df = df.astype({'holiday': 'int64', 'workingday' : 'int64', 'weather': 'int64',
        'temp' : 'float64', 'humidity':'int64', 'windspeed':'float64', 'month':'int64', 'hours':'int64', 'weekday':'int64', 'year':'int64'})

        prediction.append(int(model.predict(df)))
    
    # print(prediction)
    df_data48h['prediction'] = prediction
    heure = []
    date48 = []
    ts = df_data48h['dt']
    for correct_data in ts:
        heure.append(time.strftime("%H:%M", time.localtime(int(correct_data))))
        date48.append(time.strftime("%D", time.localtime(int(correct_data))))
    
    df_data48h['horaire'] = heure
    df_data48h['date48'] = date48
    # print(df)
    fig1 = px.histogram(df_data48h, x ="horaire", y = 'prediction', color="date48", title='prédiction sur les prochaines 48h', barmode="group")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('journalier.html', graph1JSON = graph1JSON)  

@home.route('/semaine')
def semaine_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    print('start')
    api_key_holiday= os.getenv('api_key_holiday')
    api_key = os.getenv('api_key_open_weather')
    lat = "38.89438"
    lon = "-77.03160"
    url = "http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url).json()
    temp_day = 0
    month = []
    date = []
    hours = []
    prediction = []
    temp = []
    humidity = []
    windspeed = []
    heure = []
    date48 = []
    donnee = pd.DataFrame(columns = ['holiday', 'workingday', 'weather', 'temp','humidity', 'windspeed', 'month', 'hours','weekday','year','heure','date48' ]) 
    
    for dataday in response["list"]:
        hours= time.strftime("%H", time.localtime(int(dataday['dt'])))
        month = time.strftime("%m", time.localtime(int(dataday['dt'])))
        date = time.strftime("%D", time.localtime(int(dataday['dt'])))
        temp = dataday['main']['temp']
        humidity = dataday['main']['humidity']
        windspeed =dataday['wind']['speed']
        date = pd.to_datetime(date)
        year = date.year
        weekday = date.weekday()
        heure= time.strftime("%H:%M", time.localtime(int(dataday['dt'])))
        date48= time.strftime("%D", time.localtime(int(dataday['dt'])))
        day = date.day

        climat = dataday['weather'][0]['description']
        # print(climat)
        
        if climat in list_weather1:
            weather = 1
        elif climat in list_weather2:
            weather = 2
        elif climat in list_weather3:
            weather = 3
        else:
            weather = 4
        print(weather)
        if day != temp_day:
            url_holiday = "https://holidays.abstractapi.com/v1/?api_key=%s&country=US&year=%s&month=%s&day=%s" % (api_key_holiday, year, month ,day)
            response_holiday = requests.get(url_holiday).json()
            temp_day = day

        list_working = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            
        if response_holiday =='':
            holiday = 0
            if weekday in list_working:
                workingday = 1
            else:
                workingday = 0
        else:
            holiday = 1
            workingday = 0
            
        
        to_append = [holiday, workingday, weather, temp,humidity, windspeed, month, hours,weekday,year,heure,date48]
        df_length = len(donnee)
        donnee.loc[df_length] = to_append
            

        features = [holiday, workingday, weather, temp, humidity, windspeed, month, hours,weekday,year]
        final_features = [np.array(features)]
        df = pd.DataFrame()
        df[['holiday','workingday','weather','temp','humidity','windspeed','month','hours','weekday','year']] = final_features
        df = df.astype({'holiday': 'int64', 'workingday' : 'int64', 'weather': 'int64', 
                        'temp' : 'float64', 'humidity':'int64', 'windspeed':'float64', 'month':'int64', 'hours':'int64', 'weekday':'int64', 'year':'int64'})

        prediction.append(int(model.predict(df)))
    

    donnee['prediction'] = prediction
    # print(df.shape)
    # print('**********************************************************************************************')
    # print(heure)
    # print('**********************************************************************************************')
    # print(date48)
    # print('**********************************************************************************************')
    # print(donnee)
    
    
    fig1 = px.histogram(donnee, x ="heure", y = 'prediction', color="date48", title='prédiction sur les prochaines 48h', barmode="group")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('semaine.html', graph1JSON = graph1JSON)

