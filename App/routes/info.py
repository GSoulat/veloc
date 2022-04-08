from calendar import week
import pickle
# from tkinter import X
from flask import Blueprint, request, jsonify
from flask import render_template
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
import sklearn
import requests
import json
# from dotenv import load_dotenv
import os
# load_dotenv(override=True)



info = Blueprint("info", __name__, static_folder="../static", template_folder="../templates/")

api_key_holiday= "14ae356bbffb49c58651e72ef87dbf32"
api_key = "1cf4a33bf5ed0e1005a61cb94eded3af"

@info.route('/info', methods=['get', 'post'])
def infos():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """

    return render_template('info.html') 

@info.route('/formulaire', methods = ['get', 'post'])
def formulaire():
    api_key_holiday= os.getenv('api_key_holiday')
    hours = request.form['hour']
    date = request.form['date']
    temp = request.form['temp']
    humidity = request.form['humidity']
    windspeed = request.form['windspeed']
    weather = request.form['weather']
    date = pd.to_datetime(date)
    year = date.year
    month = date.month
    weekday = date.weekday()
    date= date.date()
    day = date.day
    
    url_holiday = "https://holidays.abstractapi.com/v1/?api_key=%s&country=US&year=%s&month=%s&day=%s" % (api_key_holiday, year, month ,day)
    response_holiday = requests.get(url_holiday).json()

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
        
    data = {'holiday':holiday,'workingday': workingday, 'weather': weather,'temp': temp,'humidity': humidity,'windspeed': windspeed, 'month':month, 'hours': hours,  
              'weekday':weekday, 'year':year}
    
    # x = requests.post('http://127.0.0.1:5001/predict', json=data, headers={'Content-Type': 'application/json'})
    x = requests.post('https://apimodelveloc.azurewebsites.net/predict', json=data, headers={'Content-Type': 'application/json'})

    return render_template('date.html', prediction=x.json(), hour=hours, date=date) 



