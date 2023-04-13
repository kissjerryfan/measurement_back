from flask import Blueprint, request, render_template, g
from ..core import rfc
from . import get_data, handle_error, params_check
from werkzeug.datastructures import FileStorage

rfc_blueprint = Blueprint('rfc_blueprint', __name__, url_prefix='/rfc')


# @rfc_blueprint.before_request
# @handle_error
# def before_request():
#     get_data()


@rfc_blueprint.route('/rfc', methods=['POST'])
def handle():
    if request.method == 'POST':
        a: FileStorage = request.files.get('file')
        b = a.stream.readlines()
        return rfc.getRFC(b)
    else:
        return None

# 测试用
@rfc_blueprint.route('/hello')
def hello():
    return {'code': 200, 'data': "success! :)"}
