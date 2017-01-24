# -*- coding: utf-8 -*-

from flask import session

from client.config import Config
from client.request_api import get_api


def login_server(user_info):
    """登录服务器"""
    gender_map = {0: "N", 1: "M", 2: "F"}
    params = {
        "weixin": user_info["openid"],
        "avatar": user_info["headimgurl"],
        "nickname": user_info["nickname"],
        "gender": gender_map[int(user_info["sex"])],
        "authority": 2 # 用户
    }

    session["user"] = get_api(Config["api"]["authForWeixin"],
                          data = params)

# from flask-wechatpy, https://github.com/cloverstd/flask-wechatpy/blob/master/flask_wechatpy/__init__.py

import functools
from flask import request, current_app, abort, redirect

from wechatpy.pay import WeChatPay as ori_WeChatPay
from wechatpy.exceptions import (
    WeChatOAuthException,
)

def check_user():
    return session.get('user')

def oauth_debug(scope='snsapi_base', state=None):
    """跳过微信登录，模拟用户"""
    def decorater(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            user = check_user()
            if not user:
                user_info = Config["user_info"]
                login_server(user_info)

            return method(*args, **kwargs)
        return wrapper
    return decorater

def oauth_wechat(scope='snsapi_base', state=None):
    def decorater(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            from wechatpy.oauth import WeChatOAuth
            if callable(state):
                _state = state()
            else:
                _state = state or ''
            redirect_uri = current_app.config.get('WECHAT_OAUTH_URI')
            if not redirect_uri:
                redirect_uri = request.url
            wechat_oauth = WeChatOAuth(
                current_app.config['WECHAT_APPID'],
                current_app.config['WECHAT_SECRET'],
                redirect_uri,
                scope,
                _state
            )

            user = check_user()

            if request.args.get('code') and not user:
                try:
                    res = wechat_oauth.fetch_access_token(request.args['code'])
                except WeChatOAuthException:
                    return abort(403)
                else:
                    if scope == 'snsapi_base':
                        pass # TODO: 可不可能只获取openID
                    else:
                        user_info = wechat_oauth.get_user_info()
                        login_server(user_info)
            elif not user:
                return redirect(wechat_oauth.authorize_url)
            return method(*args, **kwargs)
        return wrapper
    return decorater

oauth = None
if Config["debug"]:
    oauth = oauth_debug
else:
    oauth = oauth_wechat


class WechatPay(object):

    def __init__(self, app=None):

        self._wechat_client = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = app.config
        config.setdefault('WECHAT_APPID', None)
        config.setdefault('WECHAT_PAY_API_KEY', None)
        config.setdefault('WECHAT_PAY_MCH_CERT', None)
        config.setdefault('WECHAT_PAY_MCH_KEY', None)
        config.setdefault('WECHAT_PAY_MCH_ID', None)
        config.setdefault('WECHAT_PAY_SUB_MCH_ID', None)

        assert config['WECHAT_APPID'] is not None
        assert config['WECHAT_PAY_API_KEY'] is not None
        assert config['WECHAT_PAY_MCH_CERT'] is not None
        assert config['WECHAT_PAY_MCH_KEY'] is not None
        assert config['WECHAT_PAY_MCH_ID'] is not None

        self._wechat_pay = ori_WeChatPay(
            appid=config['WECHAT_APPID'],
            api_key=config['WECHAT_PAY_API_KEY'],
            mch_id=config['WECHAT_PAY_MCH_ID'],
            sub_mch_id=config.get('WECHAT_PAY_SUB_MCH_ID', None),
            mch_cert=config['WECHAT_PAY_MCH_CERT'],
            mch_key=config['WECHAT_PAY_MCH_KEY'],
        )
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['wechat_pay'] = self

    def __getattr__(self, name):
        return getattr(self._wechat_pay, name)
