# -*- coding: utf-8 -*-

from flask import session
import functools

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
        return method(*args, **kwargs)

    return warpper