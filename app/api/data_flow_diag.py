from flask import Blueprint, request, render_template, g
from ..core import data_flow_diag
from . import get_data, handle_error, params_check
from werkzeug.datastructures import FileStorage

data_flow_diag_blueprint = Blueprint('data_flow_diag_blueprint', __name__, url_prefix='/data_flow_diag')


# @data_flow_diag_blueprint.before_request
# @handle_error
# def before_request():
#     get_data()


@data_flow_diag_blueprint.route('/mc', methods=['POST'])
def handle():
    if request.method == 'POST':
        print("aaa", request.files.get('file').__class__)
        a: FileStorage = request.files.get('file')
        b = a.stream.readlines()
        return data_flow_diag.getMcCabe(b)
    else:
        return None

# 测试用
@data_flow_diag_blueprint.route('/hello')
def hello():
    return {'code': 200, 'data': "success! :)"}
