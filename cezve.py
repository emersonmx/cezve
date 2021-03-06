import sys
import simplejson as json
from werkzeug.wrappers import Request as BaseRequest
from werkzeug.wrappers import Response as BaseResponse
from werkzeug.wrappers.json import JSONMixin
from werkzeug.datastructures import Headers
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import validate_arguments
from werkzeug.wsgi import ClosingIterator


class Request(BaseRequest, JSONMixin):
    pass


class Response(BaseResponse, JSONMixin):
    pass


def _endpoint_from_view_func(view_func):
    assert (
        view_func is not None
    ), 'expected view func if endpoint is not provided.'
    return view_func.__name__


def at_request_teardown(wsgi_app, teardown_list):
    def func(environ, start_response):
        return ClosingIterator(
            wsgi_app(environ, start_response), teardown_list
        )

    return func


def make_response(request, rv):
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
                'The view func did not return a valid response tuple.'
                ' The tuple must have the form (body, status, headers),'
                ' (body, status), or (body, headers).'
            )

    if rv is None:
        raise TypeError(
            f'The view function for {request.endpoint!r} did not'
            ' return a valid response. The function either returned'
            ' None or ended without a return statement.'
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
                    f'{e}\nThe view function did not return a valid'
                    ' response. The return type must be a string,'
                    ' dict, tuple, Response instance, or WSGI'
                    f' callable, but it was a {type(rv).__name__}.'
                ).with_traceback(sys.exc_info()[2])
        else:
            raise TypeError(
                'The view function did not return a valid'
                ' response. The return type must be a string,'
                ' dict, tuple, Response instance, or WSGI'
                f' callable, but it was a {type(rv).__name__}.'
            )

    if status is not None:
        if isinstance(status, (str, bytes, bytearray)):
            rv.status = status
        else:
            rv.status_code = status

    if headers:
        rv.headers.extend(headers)

    return rv


class Router(object):
    def __init__(self):
        self.url_map = Map()
        self.view_functions = {}
        self.default_methods = frozenset({'GET', 'HEAD'})
        self._fallback_func = None

    def route(self, rule, view_func, **options):
        endpoint = options.get('endpoint')
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options['endpoint'] = endpoint

        methods = options.pop('methods', self.default_methods)
        if isinstance(methods, str):
            raise TypeError(
                'Allowed methods must be a list of strings, for'
                ' example: app.route(..., methods=["POST"])'
            )
        methods = frozenset({item.upper() for item in methods})
        if methods & self.default_methods:
            methods = methods | self.default_methods

        rule = Rule(rule, methods=methods, **options)
        self.url_map.add(rule)

        if view_func is not None:
            key = (methods, endpoint)
            old_view_func = self.view_functions.get(key)
            if old_view_func is not None and old_view_func != view_func:
                raise AssertionError(
                    'View func mapping is overwriting an existing'
                    f' endpoint function: {endpoint}'
                )
            self.view_functions[key] = view_func

    def fallback(self, func):
        self._fallback_func = func

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            method = request.method
            endpoint, arguments = adapter.match(method=method)

            if method in self.default_methods:
                method = self.default_methods
            else:
                method = frozenset({method})

            view_func = self.view_functions[(method, endpoint)]
            args, kwargs = validate_arguments(
                view_func, (request, ), arguments.copy()
            )
            if len(arguments) == len(args) + len(kwargs):
                rv = view_func(**arguments)
            else:
                rv = view_func(request, **arguments)
            return make_response(request, rv)
        except NotFound as e:
            if self._fallback_func:
                return make_response(request, self._fallback_func())
            return e
        except HTTPException as e:
            return e


class Cezve(object):
    def __init__(self, router=None):
        self.router = router if router else Router()

    def route(self, rule, view_func=None, **options):
        if view_func:
            self.router.route(rule, view_func, **options)
            return

        def decorator(func):
            self.router.route(rule, func, **options)
            return func

        return decorator

    def run(self, **kwargs):
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 5000)
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger=True, use_reloader=True)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.router.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
