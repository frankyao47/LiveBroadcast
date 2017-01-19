# -*- coding: utf-8 -*-

from flask import session
import functools

from client.config import Config
from client.request_api import get_api


def login_server():
    """登录服务器"""
    gender_map = {0: "N", 1: "M", 2: "F"}
    user_info = session["user_info"]
    params = {
        "weixin": user_info["openid"],
        "avatar": user_info["headimgurl"],
        "nickname": user_info["nickname"],
        "gender": gender_map[int(user_info["sex"])]

    }
    user = get_api(Config["api"]["authForWeixin"], None,
                          params = params)

    return user


def login_tecent_IM():
    """登录腾讯IM"""
    pass


def oauth(method):
    @functools.wraps(method)
    def warpper(*args, **kwargs):
        # test user
        session["user_info"] = {
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