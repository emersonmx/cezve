from cezve import Router

path = '/test'


def callback():
    return 'test'


def test_get_setup():
    router = Router()
    router.get(path, callback)
    assert router.routes['get'][path] == callback


def test_post_setup():
    router = Router()
    router.post(path, callback)
    assert router.routes['post'][path] == callback


def test_put_setup():
    router = Router()
    router.put(path, callback)
    assert router.routes['put'][path] == callback


def test_patch_setup():
    router = Router()
    router.patch(path, callback)
    assert router.routes['patch'][path] == callback


def test_delete_setup():
    router = Router()
    router.delete(path, callback)
    assert router.routes['delete'][path] == callback


def test_options_setup():
    router = Router()
    router.options(path, callback)
    assert router.routes['options'][path] == callback


def test_match_setup():
    router = Router()
    router.match(['get', 'post'], path, callback)
    assert router.routes['get'][path] == callback
    assert router.routes['post'][path] == callback


def test_any_setup():
    router = Router()
    router.any(path, callback)
    for m in router.routes:
        assert router.routes[m][path] == callback
