from flask import Blueprint, request
from werkzeug.datastructures import FileStorage
from . import get_data, handle_error, params_check
from ..core.ast import analyze
from ..util import trueReturn, falseReturn
import traceback

ast_blueprint = Blueprint('ast_blueprint', __name__, url_prefix='/ast')


# @ast_blueprint.before_request
# @handle_error
# def before_request():
#     get_data()


@ast_blueprint.route('/metric', methods=['POST'])
def metric():
    file: FileStorage = request.files.get('file')
    content = ''.join([str(line, encoding='utf-8') for line in file.stream.readlines()])
    try:
        result = analyze(content)
        return trueReturn(data=result)
    except Exception:
        traceback.print_exc()
        return falseReturn(msg='系统错误')
