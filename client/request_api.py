# -*- coding: utf-8 -*-

import json
import requests

from flask import abort
from client.config import Config

def get_api(url, **kwargs):
    """
    API request
    """
    try:
        req = requests.post(Config["endpoint"] + url + '.action', **kwargs)
        resp = json.loads(req.content)
        errno, result = resp["errno"], resp["result"]

        if not errno:
            return result
        else:
            raise
    except Exception:
        raise
        abort(500, 'API Service is not yet open')

def get_api_complete(url, **kwargs):
    """
    API request, 返回完整的数据
    """
    try:
        req = requests.post(Config["endpoint"] + url + '.action', **kwargs)
        resp = json.loads(req.content)
        return resp
    except Exception:
        abort(500, 'API Service is not yet open')
