from cezve import Cezve

path = '/test'


def callback():
    return 'test'


def test_delegated_get_setup():
    app = Cezve()
    app.get(path, callback)
    router = app.router
    assert router.routes['get'][path] == callback


def test_delegated_post_setup():
    app = Cezve()
    app.post(path, callback)
    router = app.router
    assert router.routes['post'][path] == callback


def test_delegated_put_setup():
    app = Cezve()
    app.put(path, callback)
    router = app.router
    assert router.routes['put'][path] == callback


def test_delegated_patch_setup():
    app = Cezve()
    app.patch(path, callback)
    router = app.router
    assert router.routes['patch'][path] == callback


def test_delegated_delete_setup():
    app = Cezve()
    app.delete(path, callback)
    router = app.router
    assert router.routes['delete'][path] == callback


def test_delegated_options_setup():
    app = Cezve()
    app.options(path, callback)
    router = app.router
    assert router.routes['options'][path] == callback


def test_delegated_match_setup():
    app = Cezve()
    app.match(['get', 'post'], path, callback)
    router = app.router
    assert router.routes['get'][path] == callback
    assert router.routes['post'][path] == callback


def test_delegated_any_setup():
    app = Cezve()
    app.any(path, callback)
    router = app.router
    for m in router.routes:
        assert router.routes[m][path] == callback
