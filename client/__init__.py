# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from config import Config

app = Flask(__name__, static_url_path="")
app.config["SECRET_KEY"] = Config["SECRET_KEY"]

# 登录
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"请先登录"
login_manager.session_protection = "strong"
login_manager.init_app(app)


# 过滤器
@app.template_filter('is_url')
def is_url(s):
    return str(s).startswith("http://")

from views import *
