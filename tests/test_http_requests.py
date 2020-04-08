from werkzeug.test import Client
from cezve import Cezve, Response


def test_get_html_response():
    app = Cezve()
    app.get('/test', lambda _: 'test')
    client = Client(app, Response)

    resp = client.get('/test')

    assert resp.content_type == 'text/html'
    assert resp.data == b'test'


def test_get_json_response():
    app = Cezve()
    app.get('/test', lambda _: {'test': 'valid'})
    client = Client(app, Response)

    resp = client.get('/test')

    assert resp.content_type == 'application/json'
    assert resp.json == {'test': 'valid'}


def test_get_invalid_response():
    app = Cezve()
    app.get('/test', lambda _: 42)
    client = Client(app, Response)

    resp = client.get('/test')

    assert resp.json == 42
