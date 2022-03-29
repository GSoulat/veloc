from calendar import week
# from copyreg import pickle
import pickle
# from crypt import methods
# from unicodedata import name
from flask import Blueprint, request
from flask import render_template
from datetime import date, datetime, timedelta
# from pytz import timezone
# import requests
# import json
import pandas as pd
import numpy as np
import sklearn

info = Blueprint("info", __name__, static_folder="../static", template_folder="../templates/")
openmodel = open("App/routes/model.pkl", "rb")

model = pickle.load(openmodel)

@info.route('/info', methods=['get', 'post'])
def infos():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """

    return render_template('info.html') 

@info.route('/formulaire', methods = ['get', 'post'])
def formulaire():

    hours = request.form['hour']
    date = request.form['date']
    temp = request.form['temp']
    humidity = request.form['humidity']
    windspeed = request.form['windspeed']
    weather = request.form['weather']
    daytype = request.form['day']
    date = pd.to_datetime(date)
    month = date.month
    day_week = date.day_name()

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
    final_features = [np.array(features)]
    df = pd.DataFrame()
    df[['holiday','workingday','weather','temp','humidity','windspeed','month','hours','week']] = final_features
    df = df.astype({'holiday': 'int64', 'workingday' : 'int64', 'weather': 'int64',
    'temp' : 'float64', 'humidity':'int64', 'windspeed':'float64', 'month':'int64', 'hours':'int64'})

    prediction = model.predict(df)
    print(int(prediction))

    return render_template('date.html') 