from cezve import Router

rule = '/test'


def action():
    return 'test'


def test_basic_route():
    router = Router()
    router.route(rule, action)
    key = (router.default_methods, 'action')
    assert router.view_functions.get(key) == action
