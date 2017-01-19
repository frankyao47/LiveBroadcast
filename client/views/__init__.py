# -*- coding: utf-8 -*-

import json

from flask import render_template, abort
from client.wechatOauth import oauth
import requests

from client import app
from client.config import Config


def __get_api(url, headers, **kwargs):
    """
    API request
    """
    default_headers = {"content-type": "application/json"}
    if headers is not None and isinstance(headers, dict):
        default_headers.update(headers)
    try:
        req = requests.get(Config["endpoint"] + url + '.action', headers=default_headers, **kwargs)
        resp = json.loads(req.content)
        errno, result = resp["errno"], resp["result"]

        if not errno:
            return result
        else:
            raise
    except Exception:
        raise
        abort(500, 'API Service is not yet open')


@app.route('/show/<int:anchorUid>', methods=['GET'])
@oauth
def show(anchorUid):
    channel = __get_api(Config["api"]["getSingleChannel"], None,
                        params={"anchorUid": anchorUid})
    # __get_api(Config["api"]["getSingleChannel"], None,
    #           params={"token": "11b422634945c0b03f72101cb3eee1a7", authority: 2})
    # user = __get_api(Config["api"]["getUserInfo"], None,
    #                  params={"token": "11b422634945c0b03f72101cb3eee1a7"})
    return render_template("show.html", channel=channel)


@app.route('/', methods=['GET'])
@oauth
def index():
    channelList = __get_api(Config["api"]["getChannels"], None,
                            params={"limit": 12, "offset": 0})

    return render_template("index.html", channelList=channelList)




# @app.route('/login', methods=['GET'])
# def login():
#     """
#     微信登录跳转，用户同意后依次向私有服务器注册/登录，IM服务器注册/登录
#     """
#     pass
#
# @app.route('/listChannels', methods=['GET'])
# @oauth
# def listChannels():
#     channelList = __get_api(Config["api"]["getChannels"], None,
#                             params={"limit": 10, "offset": 0})
#     return render_template("channels.html", channelList=channelList)
#
# @app.route('/meme', methods=['GET'])
# # @login_required
# def meme():
#     channelList = __get_api(Config["api"]["getChannels"], None,
#                             params={"limit": 10, "offset": 0})
#
#     return render_template("meme.html", channelList=channelList)
