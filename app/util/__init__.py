from flask import Blueprint, jsonify


class GreenPrint(Blueprint):
    def register_blueprint(self, blueprint, **kwargs):
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (kwargs.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in kwargs:
                del kwargs['url_prefix']
            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **kwargs)
        self.record(deferred)

    def register_all(self, blueprints: list):
        for blueprint in blueprints:
            self.register_blueprint(blueprint)


def trueReturn(data=None, msg='', code=200):
    return jsonify({
        'data': data,
        'msg': msg,
        'code': code
    })


def falseReturn(data=None, msg='', code=404):
    return jsonify({
        'data': data,
        'msg': msg,
        'code': code
    })
