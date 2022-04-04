from flask import Blueprint, render_template
import requests
import pandas as pd
import time
import numpy as np
import pickle
import plotly
import plotly.express as px
import json
import plotly.express as px


home = Blueprint("home", __name__, static_folder="../static", template_folder="../templates/")

openmodel = open("App/routes/model.pkl", "rb")

model = pickle.load(openmodel)

@home.route('/')
@home.route('/home')
def home_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    
    return render_template('home.html')  

@home.route('/date')
def date_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    
    return render_template('date.html')  

@home.route('/journalier')
def journalier_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """

    api_key = "1cf4a33bf5ed0e1005a61cb94eded3af"
    lat = "38.89438"
    lon = "-77.03160"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url).json()
    prediction = []
    
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
        day_week = date.day_name()

        weather = 1
        daytype = 'day'

        if daytype == 'workingday':
            workingday = 1
            holiday = 0

        elif daytype =='holiday':
            workingday = 0
            holiday = 1
        else:
            workingday = 0
            holiday = 0       

        features = [holiday, workingday, weather, temp, humidity, windspeed, month, hours,day_week]
        # features = [temp, humidity, windspeed, month, hours,day_week]
        final_features = [np.array(features)]
        df = pd.DataFrame()
        df[['holiday','workingday','weather','temp','humidity','windspeed','month','hours','week']] = final_features
        df = df.astype({'holiday': 'int64', 'workingday' : 'int64', 'weather': 'int64',
        'temp' : 'float64', 'humidity':'int64', 'windspeed':'float64', 'month':'int64', 'hours':'int64'})

        prediction.append(int(model.predict(df)))
        # print(int(prediction))
    
    print(prediction)
    df_data48h['prediction'] = prediction
    heure = []
    date48 = []
    ts = df_data48h['dt']
    for correct_data in ts:
        heure.append(time.strftime("%H:%M", time.localtime(int(correct_data))))
        date48.append(time.strftime("%D", time.localtime(int(correct_data))))
    
    df_data48h['horaire'] = heure
    df_data48h['date48'] = date48
    
    
    fig1 = px.histogram(df_data48h, x ="horaire", y = 'prediction', color="date48", title='prédiction sur les prochaines 48h', barmode="group")
    # fig1.add_bar(df_data48h, x ="horaire", y = 'prediction', name='coint')
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # return render_template('journalier.html', tables=[df_data48h.to_html(classes='data')], titles=df_data48h.columns.values)  
    return render_template('journalier.html', graph1JSON = graph1JSON)  

@home.route('/semaine')
def semaine_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    print('start')
    api_key = "1cf4a33bf5ed0e1005a61cb94eded3af"
    lat = "38.89438"
    lon = "-77.03160"
    url = "http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url).json()
 
    month = []
    date = []
    hours = []
    prediction = []
    day_week = []
    temp = []
    humidity = []
    windspeed = []
    heure = []
    date48 = []
    donnee = pd.DataFrame(columns = ['workingday' , 'holiday', 'hours','month','date','temp','humidity','windspeed','day_week','heure','weather', 'date48' ])    
    
    for dataday in response["list"]:
        hours= time.strftime("%H", time.localtime(int(dataday['dt'])))
        month = time.strftime("%m", time.localtime(int(dataday['dt'])))
        date = time.strftime("%D", time.localtime(int(dataday['dt'])))
        temp = dataday['main']['temp']
        humidity = dataday['main']['humidity']
        windspeed =dataday['wind']['speed']
        date = pd.to_datetime(date)
        day_week = date.day_name()
        heure= time.strftime("%H:%M", time.localtime(int(dataday['dt'])))
        date48= time.strftime("%D", time.localtime(int(dataday['dt'])))

        weather = 1
        daytype = 'day'

        if daytype == 'workingday':
            workingday = 1
            holiday = 0

        elif daytype =='holiday':
            workingday = 0
            holiday = 1
        else:
            workingday = 0
            holiday = 0
            
        
        to_append = [workingday , holiday, hours,month,date,temp,humidity,windspeed,day_week,heure,weather,date48]
        df_length = len(donnee)
        donnee.loc[df_length] = to_append
            
        # print(donnee)

        features = [holiday, workingday, weather, temp, humidity, windspeed, month, hours,day_week]
        final_features = [np.array(features)]
        df = pd.DataFrame()
        df[['holiday','workingday','weather','temp','humidity','windspeed','month','hours','week']] = final_features
        df = df.astype({'holiday': 'int64', 'workingday' : 'int64', 'weather': 'int64', 
                        'temp' : 'float64', 'humidity':'int64', 'windspeed':'float64', 'month':'int64', 'hours':'int64'})

        prediction.append(int(model.predict(df)))
    

    
    print(df.shape)
    print('**********************************************************************************************')
    print(heure)
    print('**********************************************************************************************')
    print(date48)
    print('**********************************************************************************************')
    print(donnee)
    donnee['prediction'] = prediction
    
    fig1 = px.histogram(donnee, x ="heure", y = 'prediction', color="date48", title='prédiction sur les prochaines 48h', barmode="group")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('semaine.html', graph1JSON = graph1JSON)

