import sys
import simplejson as json
from werkzeug.wrappers import Request as BaseRequest
from werkzeug.wrappers import Response as BaseResponse
from werkzeug.wrappers.json import JSONMixin
from werkzeug.datastructures import Headers


class Router(object):
    def __init__(self):
        self.routes = {}

    def route(self, uri, action, **options):
        self.routes[uri] = action

    def dispatch_request(self, request):
        action = self.routes.get(request.path)
        return action(request)


class Request(BaseRequest, JSONMixin):
    pass


class Response(BaseResponse, JSONMixin):
    pass


class Cezve(object):
    def __init__(self, router=Router()):
        self.router = router

    def route(self, uri, action=None, **options):
        if action:
            self.router.route(uri, action, **options)
            return

        def decorator(action):
            self.router.route(uri, action, **options)
            return action

        return decorator

    def run(self, **kwargs):
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 5000)
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger=True, use_reloader=True)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        rv = self.router.dispatch_request(request)
        response = self.make_response(request, rv)
        return response(environ, start_response)

    def make_response(self, request, rv):
        status = headers = None
        if isinstance(rv, tuple):
            len_rv = len(rv)
            if len_rv == 3:
                rv, status, header = rv
            elif len_rv == 2:
                if isinstance(rv[1], (Headers, dict, tuple, list)):
                    rv, headers = rv
                else:
                    rv, status = rv
            else:
                raise TypeError(
                    "The action did not return a valid response tuple."
                    " The tuple must have the form (body, status, headers),"
                    " (body, status), or (body, headers)."
                )

        if rv is None:
            raise TypeError(
                f"The view function for {request.endpoint!r} did not"
                " return a valid response. The function either returned"
                " None or ended without a return statement."
            )

        if not isinstance(rv, Response):
            if isinstance(rv, (str, bytes, bytearray)):
                rv = Response(rv, status=status, headers=headers)
                status = headers = None
            elif isinstance(rv, dict):
                rv = Response(json.dumps(rv), mimetype='application/json')
            elif isinstance(rv, BaseResponse) or callable(rv):
                try:
                    rv = Response.force_type(rv, request.environ)
                except TypeError as e:
                    raise TypeError(
                        f"{e}\nThe view function did not return a valid"
                        " response. The return type must be a string,"
                        " dict, tuple, Response instance, or WSGI"
                        f" callable, but it was a {type(rv).__name__}."
                    ).with_traceback(sys.exc_info()[2])
            else:
                raise TypeError(
                    "The view function did not return a valid"
                    " response. The return type must be a string,"
                    " dict, tuple, Response instance, or WSGI"
                    f" callable, but it was a {type(rv).__name__}."
                )

        if status is not None:
            if isinstance(status, (str, bytes, bytearray)):
                rv.status = status
            else:
                rv.status_code = status

        if headers:
            rv.headers.extend(headers)

        return rv

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
