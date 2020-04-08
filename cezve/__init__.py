import simplejson as json
from werkzeug.wrappers import Request as BaseRequest
from werkzeug.wrappers import Response as BaseResponse
from werkzeug.wrappers.json import JSONMixin


class Request(BaseRequest, JSONMixin):
    pass


class Response(BaseResponse, JSONMixin):
    pass


def get_json(data):
    try:
        return json.dumps(data)
    except (TypeError, OverflowError):
        return None


class Router(object):
    def __init__(self):
        self.routes = {}

    def get(self, expr, callback):
        routes = self.routes.setdefault('get', {})
        routes[expr] = callback
        return self

    def post(self, expr, callback):
        routes = self.routes.setdefault('post', {})
        routes[expr] = callback
        return self

    def put(self, expr, callback):
        routes = self.routes.setdefault('put', {})
        routes[expr] = callback
        return self

    def patch(self, expr, callback):
        routes = self.routes.setdefault('patch', {})
        routes[expr] = callback
        return self

    def delete(self, expr, callback):
        routes = self.routes.setdefault('delete', {})
        routes[expr] = callback
        return self

    def options(self, expr, callback):
        routes = self.routes.setdefault('options', {})
        routes[expr] = callback
        return self

    def match(self, methods, expr, callback):
        for method in methods:
            getattr(self, method.lower())(expr, callback)
        return self

    def any(self, expr, callback):
        methods = ['get', 'post', 'put', 'patch', 'delete', 'options']
        self.match(methods, expr, callback)
        return self

    def _get_callback(self, method, expr):
        routes = self.routes.get(method, {})
        return routes.get(expr, None)


class Cezve(object):
    def __init__(self, router=Router()):
        self.router = router

    def get(self, expr, callback):
        self.router.get(expr, callback)
        return self

    def post(self, expr, callback):
        self.router.post(expr, callback)
        return self

    def put(self, expr, callback):
        self.router.put(expr, callback)
        return self

    def patch(self, expr, callback):
        self.router.patch(expr, callback)
        return self

    def delete(self, expr, callback):
        self.router.delete(expr, callback)
        return self

    def options(self, expr, callback):
        self.router.options(expr, callback)
        return self

    def match(self, methods, expr, callback):
        self.router.match(methods, expr, callback)
        return self

    def any(self, expr, callback):
        self.router.any(expr, callback)
        return self

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self._dispatch_request(request)

        if isinstance(response, str):
            response = Response(response)
            response.content_type = 'text/html'
            return response(environ, start_response)

        if isinstance(response, BaseResponse):
            return response(environ, start_response)

        json_data = get_json(response)
        if json_data:
            response = Response(json_data)
            response.content_type = 'application/json'
            return response(environ, start_response)

        # raise error

    def _dispatch_request(self, request):
        method = request.method.lower()
        callback = self.router._get_callback(method, request.path)
        return callback(request)

    def run(self, **kwargs):
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 5000)
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger=True, use_reloader=True)
