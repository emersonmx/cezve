from werkzeug.test import Client
from cezve import Cezve, Response


def test_between_different_methods():
    app = Cezve()
    router = app.router
    router.route('/', lambda: 'index', endpoint='index')
    router.route('/create', lambda: 'create', endpoint='create')
    router.route('/', lambda: 'store', methods=['post'], endpoint='store')
    router.route('/<i>', lambda i: 'show', endpoint='show')
    router.route('/<i>/edit', lambda i: 'edit', endpoint='edit')
    router.route('/<i>', lambda i: 'put', methods=['put'], endpoint='put')
    router.route(
        '/<i>', lambda i: 'patch', methods=['patch'], endpoint='patch'
    )
    router.route(
        '/<i>', lambda i: 'delete', methods=['delete'], endpoint='delete'
    )

    client = Client(app, Response)
    resp = client.get('/')
    assert resp.data == b'index'
    resp = client.get('/create')
    assert resp.data == b'create'
    resp = client.post('/')
    assert resp.data == b'store'
    resp = client.get('/1')
    assert resp.data == b'show'
    resp = client.get('/1/edit')
    assert resp.data == b'edit'
    resp = client.put('/1')
    assert resp.data == b'put'
    resp = client.patch('/1')
    assert resp.data == b'patch'
    resp = client.delete('/1')
    assert resp.data == b'delete'
