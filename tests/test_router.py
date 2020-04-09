from cezve import Router

uri = '/test'


def action():
    return 'test'


def test_get_setup():
    router = Router()
    route = router.get(uri, action)
    assert route == {'methods': ('GET', 'HEAD'), 'uri': uri, 'action': action}
    assert router.get_action('GET', uri) == action
    assert router.get_action('HEAD', uri) == action


def test_post_setup():
    router = Router()
    route = router.post(uri, action)
    assert route == {'methods': ('POST', ), 'uri': uri, 'action': action}
    assert router.get_action('POST', uri) == action


def test_put_setup():
    router = Router()
    route = router.put(uri, action)
    assert route == {'methods': ('PUT', ), 'uri': uri, 'action': action}
    assert router.get_action('PUT', uri) == action


def test_patch_setup():
    router = Router()
    route = router.patch(uri, action)
    assert route == {'methods': ('PATCH', ), 'uri': uri, 'action': action}
    assert router.get_action('PATCH', uri) == action


def test_delete_setup():
    router = Router()
    route = router.delete(uri, action)
    assert route == {'methods': ('DELETE', ), 'uri': uri, 'action': action}
    assert router.get_action('DELETE', uri) == action


def test_options_setup():
    router = Router()
    route = router.options(uri, action)
    assert route == {'methods': ('OPTIONS', ), 'uri': uri, 'action': action}
    assert router.get_action('OPTIONS', uri) == action
