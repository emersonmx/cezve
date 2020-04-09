from werkzeug.test import Client
from cezve import Cezve, Response


def test_html_response():
    app = Cezve()
    app.get('/test', lambda _: 'test')

    client = Client(app, Response)
    resp = client.get('/test')

    assert resp.content_type == 'text/html'
    assert resp.data == b'test'


def test_json_response():
    app = Cezve()
    app.get('/test', lambda _: {'test': 'valid'})

    client = Client(app, Response)
    resp = client.get('/test')

    assert resp.is_json
    assert resp.json == {'test': 'valid'}


def test_numeric_response():
    app = Cezve()
    app.get('/test', lambda _: 42)

    client = Client(app, Response)
    resp = client.get('/test')

    assert resp.is_json
    assert resp.json == 42


def test_response():
    app = Cezve()
    response = Response('test')
    app.get('/test', lambda _: response)

    client = Client(app, Response)
    resp = client.get('/test')

    assert resp.data == response.data