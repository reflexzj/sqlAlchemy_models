# coding=utf-8
# from flask import Flask
# app = Flask(__name__)
from main_codes import app
# from laws_models import *
from create_databases import *

@app.route('/')
def hello_world():
    return 'Hello World!'


