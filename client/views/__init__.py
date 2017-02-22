# -*- coding: utf-8 -*-

import flask
from flask import render_template, session, request
from client.wechat import oauth

from client import app
from client.config import Config
from client.request_api import get_api, get_api_complete

@app.route('/show/<int:anchorUid>', methods=['GET'])
@oauth(scope="snsapi_userinfo")
def show(anchorUid):
    channel = get_api(Config["api"]["getSingleChannel"],
                        data={"anchorUid": anchorUid, "token": session["user"]["token"]})

    giftList = get_api(Config["api"]["getGiftModels"],
                       data={"token": session["user"]["token"]})

    user = get_api(Config["api"]["getMyInfo"],
                       data={"token": session["user"]["token"]})

    cost, ifPay = channel["cost"], channel["ifPay"]
    if cost < 1 or ifPay: # 直播间免费or用户已付费
        return render_template("show.html", channel=channel, giftList=giftList, user=user, userSig = session["user"]["usersig"])
    else:
        return render_template("remind_pay.html", channel=channel, next=request.url, cost=cost, money=user["money"])

@app.route('/', methods=['GET'])
@oauth(scope="snsapi_userinfo")
def index():
    channelList = get_api(Config["api"]["getChannels"],
                            data={"limit": 12, "offset": 0})

    user = get_api(Config["api"]["getMyInfo"],
                   data={"token": session["user"]["token"]})

    return render_template("index.html", channelList=channelList, user=user)


@app.route('/pay/', methods=['GET'])
@oauth(scope="snsapi_userinfo")
def pay():
    user = get_api(Config["api"]["getMyInfo"],
                   data={"token": session["user"]["token"]})

    signature = get_api(Config["api"]["getSignatureForJs"],
                   data={"url": request.url})

    return render_template("pay.html", user=user, signature=signature)


@app.route('/api', methods=['POST'])
@oauth(scope="snsapi_userinfo")
def api():
    params = request.form.to_dict()
    action = params.get("action")
    params.pop("action")
    params["token"] = session["user"]["token"]
    result = get_api_complete(Config["api"][action],
                             data=params)

    return flask.jsonify(**result)






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
