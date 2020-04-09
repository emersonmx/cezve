import re
import simplejson as json
from werkzeug.wrappers import Request as BaseRequest
from werkzeug.wrappers import Response as BaseResponse
from werkzeug.wrappers.json import JSONMixin


class Router(object):
    def __init__(self):
        self.routes = {}
        self._verbs = (
            'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'
        )

    def get(self, uri, action):
        return self._add_route(('GET', 'HEAD'), uri, action)

    def post(self, uri, action):
        return self._add_route(('POST', ), uri, action)

    def put(self, uri, action):
        return self._add_route(('PUT', ), uri, action)

    def patch(self, uri, action):
        return self._add_route(('PATCH', ), uri, action)

    def delete(self, uri, action):
        return self._add_route(('DELETE', ), uri, action)

    def options(self, uri, action):
        return self._add_route(('OPTIONS', ), uri, action)

    def get_action(self, method: str, uri: str):
        get_methods = ('GET', 'HEAD')
        method = get_methods if method in get_methods else (method, )
        methods = self.routes.get(uri, {})
        route = methods.get(method, {})
        return route.get('action', None)

    def _add_route(self, methods, uri, action):
        route = self._create_route(methods, uri, action)
        self.routes[uri] = {route['methods']: route}
        return route

    def _create_route(self, methods, uri, action):
        return {'methods': methods, 'uri': uri, 'action': action}


def get_json(data):
    try:
        return json.dumps(data)
    except (TypeError, OverflowError):
        return None


class Request(BaseRequest, JSONMixin):
    pass


class Response(BaseResponse, JSONMixin):
    pass


class Cezve(object):
    def __init__(self, router=Router()):
        self.router = router

    def get(self, uri, action):
        self.router.get(uri, action)
        return self

    def post(self, uri, action):
        self.router.post(uri, action)
        return self

    def put(self, uri, action):
        self.router.put(uri, action)
        return self

    def patch(self, uri, action):
        self.router.patch(uri, action)
        return self

    def delete(self, uri, action):
        self.router.delete(uri, action)
        return self

    def options(self, uri, action):
        self.router.options(uri, action)
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
        method = request.method.upper()
        action = self.router.get_action(method, request.path)
        return action(request)

    def run(self, **kwargs):
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 5000)
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger=True, use_reloader=True)
