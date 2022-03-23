from crypt import methods
from flask import Blueprint, request
from flask import render_template
from datetime import date, datetime, timedelta
from pytz import timezone
import requests
import json

info = Blueprint("info", __name__, static_folder="../static", template_folder="../templates/")



@info.route('/info', methods=['get', 'post'])
def infos():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """

    return render_template('info.html') 

@info.route('/formulaire', methods = ['get', 'post'])
def formulaire():
    date = request.form('date')
    print('date: ', date)

    return render_template('info.html') 