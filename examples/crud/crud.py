import os
import sqlite3
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound
from werkzeug.local import Local, LocalManager
from cezve import Cezve, Request, Response, at_request_teardown

local = Local()
local_manager = LocalManager([local])

TEMPLATE_PATH = os.path.dirname(__file__)
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_PATH), autoescape=True
)


def render_template(name, **context):
    t = jinja_env.get_template(name)
    return Response(t.render(context), mimetype='text/html')


def get_db():
    if 'db' not in local:
        local.db = sqlite3.connect(
            'crud.sqlite', detect_types=sqlite3.PARSE_DECLTYPES
        )
        local.db.row_factory = sqlite3.Row

    return local.db


def close_db():
    db = getattr(local, 'db', None)
    if db is not None:
        db.close()


def index():
    contents = get_db().execute('SELECT * FROM contents').fetchall()
    return render_template('index.html', contents=contents)


def create():
    return render_template('create.html')


def store(req: Request):
    db = get_db()
    db.execute(
        'INSERT INTO contents (title, body, created_at) VALUES (?, ?, ?)', (
            req.form['title'], req.form['body'],
            datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        )
    )
    db.commit()
    return redirect('/')


def edit(req, content_id):
    content = get_db().execute(
        'SELECT * FROM contents WHERE id = ?', (content_id, )
    ).fetchone()
    if not content:
        raise NotFound
    return render_template('edit.html', content=content)


def update(req, content_id):
    db = get_db()
    content = db.execute(
        'SELECT * FROM contents WHERE id = ?', (content_id, )
    ).fetchone()
    if not content:
        raise NotFound

    db.execute(
        'UPDATE contents '
        'SET title = ?, body = ?, updated_at = ?'
        'WHERE id = ?', (
            req.form['title'], req.form['body'],
            datetime.today().strftime('%Y-%m-%d %H:%M:%S'), content_id
        )
    )
    db.commit()

    return redirect('/{}/edit'.format(content_id))


def destroy(content_id):
    db = get_db()
    content = db.execute(
        'SELECT * FROM contents WHERE id = ?', (content_id, )
    ).fetchone()
    if not content:
        raise NotFound

    db.execute('DELETE FROM contents WHERE id = ?', (content_id, ))
    db.commit()

    return Response(status=204)


app = Cezve()
app.wsgi_app = at_request_teardown(app.wsgi_app, [close_db])
app.wsgi_app = local_manager.make_middleware(app.wsgi_app)
app.route('/', index)
app.route('/create', create)
app.route('/', store, methods=['post'])
app.route('/<int:content_id>/edit', edit)
app.route('/<int:content_id>', update, methods=['post'])
app.route('/<int:content_id>', destroy, methods=['delete'])
app.router.fallback(lambda: ("Something wrong can't be right!", 404))
app.run()
