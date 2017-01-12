# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config["SECRET_KEY"] = Config["SECRET_KEY"]

# 登录
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"请先登录"
login_manager.session_protection = "strong"
login_manager.init_app(app)


from views import *
