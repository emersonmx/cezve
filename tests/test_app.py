from werkzeug.test import Client
from cezve import Cezve, Response


def test_app_simple_route():
    def action():
        return 'test'

    app = Cezve()
    app.route('/test', action)

    client = Client(app, Response)
    resp = client.get('/test')

    assert resp.data == b'test'


def test_app_decorated_route():
    app = Cezve()

    @app.route('/test')
    def action():
        return 'test'

    client = Client(app, Response)
    resp = client.get('/test')

    assert resp.data == b'test'
