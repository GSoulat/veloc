from calendar import week
import pickle
from tkinter import X
from flask import Blueprint, request, jsonify
from flask import render_template
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
import sklearn
import requests
import json


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
    year = date.year
    month = date.month
    weekday = date.weekday()
    date= date.date()
    if daytype == 'workingday':
        workingday = 1
        holiday = 0

    elif daytype =='holiday':
        workingday = 0
        holiday = 1
    else:
        workingday = 0
        holiday = 0
        
    data = {'holiday':holiday,'workingday': workingday, 'weather': weather,'temp': temp,'humidity': humidity,'windspeed': windspeed, 'month':month, 'hours': hours,  
              'weekday':weekday, 'year':year}
    
    print('data : ', data)
    x = requests.post('http://localhost:5001/predict', json=data,
            headers={'Content-Type': 'application/json'})
    
    print(' x : ', x.json())

    return render_template('date.html', prediction=x.json(), hour=hours, date=date) 



