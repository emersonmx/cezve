import simplejson as json
from werkzeug.wrappers import Request as BaseRequest
from werkzeug.wrappers import Response as BaseResponse
from werkzeug.wrappers.json import JSONMixin


class Router(object):
    def __init__(self):
        self.routes = {}

    def route(self, uri, action):
        self.routes[uri] = action

    def get_action(self, uri):
        return self.routes.get(uri)


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

    def run(self, **kwargs):
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 5000)
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger=True, use_reloader=True)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)

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

    def dispatch_request(self, request):
        action = self.router.get_action(request.path)
        return action(request)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
