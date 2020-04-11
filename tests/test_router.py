from cezve import Router

rule = '/test'


def action():
    return 'test'


def test_basic_route():
    router = Router()
    router.route(rule, action)
    assert router.view_functions.get('action') == action
