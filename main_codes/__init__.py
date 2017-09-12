# coding=utf-8
from main_codes.apps import create_app
from main_codes.settings import Config
from flask_sqlalchemy import SQLAlchemy

app = create_app(Config)
db = SQLAlchemy(app)

# 加载定义好的模型，不可缺少
from . import data_models