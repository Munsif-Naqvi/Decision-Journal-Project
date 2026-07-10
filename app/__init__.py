# WIRES EVERYTHING TOGETHER
from flask import Flask

from app.users.routes import users_bp
from config import config_by_name
from app.extensions.db import db
from app.extensions.migrate import migrate


def create_app(config_name='development'):
    app = Flask(__name__)
    app.json.sort_keys = False
    # copies only the UPPER cased class attributes defined in the 'config_name' variable
    # to the 'app.config' to configure the environment

    app.config.from_object(config_by_name[config_name])

    db.init_app(app) # 'db' here is an instance of [db = SQLAlchemy()], not db.py
    migrate.init_app(app, db)

    from app import models

    app.register_blueprint(users_bp, url_prefix='/api/v1/users')


    return app