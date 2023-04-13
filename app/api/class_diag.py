from flask import Blueprint, request
from . import get_data, handle_error, params_check
from ..util import trueReturn, falseReturn
from ..core import class_diag
from werkzeug.datastructures import FileStorage

class_diag_blueprint = Blueprint('class_diag_blueprint', __name__, url_prefix='/class_diag')


# @class_diag_blueprint.before_request
# @handle_error
# def before_request():
#     get_data()

@class_diag_blueprint.route('/artoria', methods=['POST'])
def handle():
    if request.method == 'POST':
        a: FileStorage = request.files.get('file')
        b = a.stream.readlines()
        return class_diag.getData(b)
    else:
        return None

# 测试用
@class_diag_blueprint.route('/test', methods=['GET'])
def trial():
    return {'code': 200, 'msg': "Use Case Hello :)"}