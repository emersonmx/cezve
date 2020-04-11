import pytest
from cezve import Router

rule = '/test'


def action():
    return 'test'


def test_basic_route():
    router = Router()
    router.route(rule, action)
    key = (router.default_methods, 'action')
    assert router.view_functions.get(key) == action


def test_if_methods_is_string():
    router = Router()
    with pytest.raises(TypeError, match='example: app.route'):
        router.route('/', lambda: 'test', methods='get')
