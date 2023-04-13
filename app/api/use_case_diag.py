from flask import Blueprint, request
from ..core import use_case_diag
from . import get_data, handle_error, params_check
from werkzeug.datastructures import FileStorage

use_case_diag_blueprint = Blueprint('use_case_diag_blueprint', __name__, url_prefix='/use_case_diag')


# @use_case_diag_blueprint.before_request
# @handle_error
# def before_request():
#     get_data()


@use_case_diag_blueprint.route('/ava', methods=['POST'])
def handle():
    if request.method == 'POST':
        a: FileStorage = request.files.get('file')
        b = a.stream.readlines()
        return use_case_diag.getActorandUseCase(b)
    else:
        return None

# 测试用
@use_case_diag_blueprint.route('/trial', methods=['GET'])
def trial():
    return {'code': 200, 'msg': "Use Case Hello :)"}
