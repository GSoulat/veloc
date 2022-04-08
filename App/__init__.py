from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv(override=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    
    # from . import models
    from .routes import home
    from .routes import info
    api_key_holiday = os.getenv('api_key_holiday')
    api_key = os.getenv('api_key_open_weather')
	# blueprint for auth routes in our app
    app.register_blueprint(home.home)
    app.register_blueprint(info.info)
    
    return app

app = create_app()

