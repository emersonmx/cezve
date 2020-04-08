import json
from werkzeug.wrappers import Request, Response


class Router(object):
    def __init__(self):
        self.routes = {}

    def get(self, path, callback):
        routes = self.routes.setdefault('get', {})
        routes[path] = callback
        return self

    def post(self, path, callback):
        routes = self.routes.setdefault('post', {})
        routes[path] = callback
        return self

    def put(self, path, callback):
        routes = self.routes.setdefault('put', {})
        routes[path] = callback
        return self

    def patch(self, path, callback):
        routes = self.routes.setdefault('patch', {})
        routes[path] = callback
        return self

    def delete(self, path, callback):
        routes = self.routes.setdefault('delete', {})
        routes[path] = callback
        return self

    def options(self, path, callback):
        routes = self.routes.setdefault('options', {})
        routes[path] = callback
        return self

    def match(self, methods, path, callback):
        for method in methods:
            getattr(self, method)(path, callback)
        return self

    def any(self, path, callback):
        methods = ['get', 'post', 'put', 'patch', 'delete', 'options']
        self.match(methods, path, callback)
        return self

    def _get_callback(self, method, path):
        routes = self.routes.get(method, {})
        return routes.get(path, None)


class Cezve(object):
    def __init__(self):
        self.router = Router()

    def get(self, path, callback):
        self.router.get(path, callback)
        return self

    def post(self, path, callback):
        self.router.post(path, callback)
        return self

    def put(self, path, callback):
        self.router.put(path, callback)
        return self

    def patch(self, path, callback):
        self.router.patch(path, callback)
        return self

    def delete(self, path, callback):
        self.router.delete(path, callback)
        return self

    def options(self, path, callback):
        self.router.options(path, callback)
        return self

    def match(self, methods, path, callback):
        self.router.match(methods, path, callback)
        return self

    def any(self, path, callback):
        self.router.any(path, callback)
        return self

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self._dispatch_request(request)

        if isinstance(response, str):
            response = Response(response)
        elif isinstance(response, dict):
            response = Response(json.dumps(response))

        return response(environ, start_response)

    def _dispatch_request(self, request):
        method = request.method.lower()
        callback = self.router._get_callback(method, request.path)
        return callback(request)

    def run(self, **kwargs):
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 5000)
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger=True, use_reloader=True)
