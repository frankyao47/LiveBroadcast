# -*- coding: utf-8 -*-

from flask import render_template, session
from client.wechatOauth import oauth

from client import app
from client.config import Config
from client.request_api import get_api

@app.route('/show/<int:anchorUid>', methods=['GET'])
@oauth
def show(anchorUid):
    channel = get_api(Config["api"]["getSingleChannel"], None,
                        params={"anchorUid": anchorUid})
    # __get_api(Config["api"]["getSingleChannel"], None,
    #           params={"token": "11b422634945c0b03f72101cb3eee1a7", authority: 2})
    # user = __get_api(Config["api"]["getUserInfo"], None,
    #                  params={"token": "11b422634945c0b03f72101cb3eee1a7"})
    return render_template("show.html", channel=channel, user=session["user"])


@app.route('/', methods=['GET'])
@oauth
def index():
    channelList = get_api(Config["api"]["getChannels"], None,
                            params={"limit": 12, "offset": 0})

    return render_template("index.html", channelList=channelList, user=session["user"])




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
