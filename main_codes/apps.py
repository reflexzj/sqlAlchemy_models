from flask import Flask
from main_codes.extensions import db


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    # error: application not registered on db instance and no applicationbound to current context
    # db.init_app(app)
    return app