from cezve import Router

uri = '/test'


def action():
    return 'test'


def test_basic_route():
    router = Router()
    router.route(uri, action)
    assert router.actions.get('action') == action
