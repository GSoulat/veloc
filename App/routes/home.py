from flask import Blueprint
from flask import render_template
from datetime import datetime, timedelta
from pytz import timezone
import requests
import json

home = Blueprint("home", __name__, static_folder="../static", template_folder="../templates/")

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
    lat = "50.62925"
    lon = "3.057256"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
    response = requests.get(url).json()
    print(response)
    
    
    
    return render_template('journalier.html', data=response)  


@home.route('/semaine')
def semaine_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    
    return render_template('semaine.html')  
