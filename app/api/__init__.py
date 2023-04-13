from functools import wraps
from ..util import falseReturn
from flask import g, request
import traceback
import json


def handle_error(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        # noinspection PyBroadException
        try:
            return func(*args, **kwargs)
        except:
            print(traceback.format_exc())
            return falseReturn(None, '服务器错误，请检查')
    return decorator


def get_data():
    if (request.method == 'POST' or request.method == 'PUT') and request.get_data():
        g.data = request.get_json()
    elif request.method == 'GET' or request.method == 'DELETE':
        g.data = request.args
    else:
        g.data = {}


def params_check(params: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            param_missing = []
            for param in params:
                if param not in g.data:
                    param_missing.append(param)
            if len(param_missing) > 0:
                return falseReturn(msg='缺少参数: %s' % json.dumps(param_missing, ensure_ascii=False))
            return func(*args, **kwargs)
        return wrapper
    return decorator
