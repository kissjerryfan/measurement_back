from flask import Flask
from flask_cors import CORS
from .util import GreenPrint


def create_app() -> Flask:
    flask_app = Flask(__name__)

    ctx = flask_app.app_context()
    ctx.push()
    CORS(flask_app, support_credentials=True, cors_allowed_origins='*')

    api = register()
    flask_app.register_blueprint(api)
    return flask_app


def register():
    from .api import ast, class_diag, data_flow_diag, use_case_diag, loc, rfc

    api = GreenPrint('api', __name__, url_prefix='/api')
    api.register_all([
        ast.ast_blueprint,
        class_diag.class_diag_blueprint,
        data_flow_diag.data_flow_diag_blueprint,
        use_case_diag.use_case_diag_blueprint,
        loc.loc_blueprint,
        rfc.rfc_blueprint
    ])
    return api
