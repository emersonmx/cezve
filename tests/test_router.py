from cezve import Router

uri = '/test'


def action():
    return 'test'


def test_basic_route():
    router = Router()
    router.route(uri, action)
    assert router.get_action(uri) == action
