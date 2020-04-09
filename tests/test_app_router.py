from cezve import Router

uri = '/test'


def action():
    return 'test'


def test_delegate_get_setup():
    router = Router()
    router.get(uri, action)
    assert router.get_action('GET', uri) == action
    assert router.get_action('HEAD', uri) == action


def test_delegate_post_setup():
    router = Router()
    router.post(uri, action)
    assert router.get_action('POST', uri) == action


def test_delegate_put_setup():
    router = Router()
    router.put(uri, action)
    assert router.get_action('PUT', uri) == action


def test_delegate_patch_setup():
    router = Router()
    router.patch(uri, action)
    assert router.get_action('PATCH', uri) == action


def test_delegate_delete_setup():
    router = Router()
    router.delete(uri, action)
    assert router.get_action('DELETE', uri) == action


def test_delegate_options_setup():
    router = Router()
    router.options(uri, action)
    assert router.get_action('OPTIONS', uri) == action
