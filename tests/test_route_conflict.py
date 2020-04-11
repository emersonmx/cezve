from werkzeug.test import Client
from cezve import Cezve, Response


def test_between_different_methods():
    app = Cezve()
    router = app.router
    router.route('/', lambda: 'index', endpoint='index')
    router.route('/', lambda: 'store', methods=['POST'], endpoint='store')

    client = Client(app, Response)
    resp = client.get('/')
    assert resp.data == b'index'
    resp = client.post('/')
    assert resp.data == b'store'
