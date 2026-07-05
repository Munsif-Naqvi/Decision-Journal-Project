from flask import Flask
from config import config_by_name

def create_app(config_name='development'):
    app = Flask(__name__)

    # copies only the UPPER cased class attributes defined in the 'config_name' variable
    # to the 'app.config' to configure the environment

    app.config.from_object(config_by_name[config_name])

    @app.get('/health_check')
    def health_check():
        return {"status": "ok"}

    return app