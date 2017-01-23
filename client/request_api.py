# -*- coding: utf-8 -*-

import json
import requests

from flask import abort
from client.config import Config

def get_api(url, headers, **kwargs):
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

def get_api_complete(url, headers, **kwargs):
    """
    API request, 返回完整的数据
    """
    default_headers = {"content-type": "application/json"}
    if headers is not None and isinstance(headers, dict):
        default_headers.update(headers)
    try:
        req = requests.get(Config["endpoint"] + url + '.action', headers=default_headers, **kwargs)
        resp = json.loads(req.content)
        return resp
    except Exception:
        abort(500, 'API Service is not yet open')
