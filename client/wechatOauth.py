# -*- coding: utf-8 -*-

from flask import session
import functools


def login_server():
    """登录服务器"""
    pass


def login_tecent_IM():
    """登录腾讯IM"""
    pass


def oauth(method):
    @functools.wraps(method)
    def warpper(*args, **kwargs):
        # test user
        session['user_info'] = {
            "openid": "test123",
            "nickname": "Frank",
            "sex": "1",
            "province": "PROVINCE",
            "city":"CITY",
            "country":"COUNTRY",
            "headimgurl": "http://localhost:5000",
            "privilege":[
            ]
        }

        login_server()
        login_tecent_IM()

        return method(*args, **kwargs)

    return warpper