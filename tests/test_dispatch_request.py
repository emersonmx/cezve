import pytest
from werkzeug.test import Client
from cezve import Cezve, Request, Response


def test_if_has_request():
    app = Cezve()
    client = Client(app, Response)
    app.route('/test', lambda req: 'test')
    resp = client.get('/test')
    assert resp.data == b'test'


def test_if_has_not_request():
    app = Cezve()
    client = Client(app, Response)
    app.route('/test', lambda: 'test')
    resp = client.get('/test')
    assert resp.data == b'test'


def test_if_has_request_and_arg():
    app = Cezve()
    client = Client(app, Response)
    app.route('/test/<a>', lambda r, a: 'test')
    resp = client.get('/test/hello')
    assert resp.data == b'test'


def test_if_arg_value_is_ok():
    app = Cezve()
    client = Client(app, Response)
    app.route('/test/<a>', lambda a: a)
    resp = client.get('/test/hello')
    assert resp.data == b'hello'


def test_if_args_values_are_ok():
    app = Cezve()
    client = Client(app, Response)
    app.route('/test/<a>/<b>', lambda a, b: {'values': [a, b]})
    resp = client.get('/test/hello/world')
    assert resp.json == {'values': ['hello', 'world']}


def test_if_request_and_arg_values_are_ok():
    app = Cezve()
    client = Client(app, Response)
    app.route('/test/<a>', lambda r, a: {'r': type(r).__name__, 'a': a})
    resp = client.get('/test/hello')
    assert resp.json == {'r': Request.__name__, 'a': 'hello'}


def test_if_request_and_args_values_are_ok():
    app = Cezve()
    client = Client(app, Response)
    app.route(
        '/test/<a>/<b>', lambda r, a, b: {
            'r': type(r).__name__,
            'a': a,
            'b': b
        }
    )
    resp = client.get('/test/hello/world')
    assert resp.json == {'r': Request.__name__, 'a': 'hello', 'b': 'world'}


def test_if_arg_key_is_the_same():
    app = Cezve()
    client = Client(app, Response)
    app.route('/test/<key>', lambda e: e)
    with pytest.raises(
        TypeError, match="got an unexpected keyword argument 'key'"
    ):
        client.get('/test/hello')


def test_if_args_keys_are_the_same():
    app = Cezve()
    client = Client(app, Response)
    app.route('/test/<key1>/<key2>', lambda a, b: 'ignore')
    with pytest.raises(
        TypeError, match="got an unexpected keyword argument 'key"
    ):
        client.get('/test/hello/world')
