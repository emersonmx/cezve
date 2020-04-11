import os
from datetime import datetime
from cezve import Cezve, Request, Response
from jinja2 import Environment, FileSystemLoader
from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

TEMPLATE_PATH = os.path.dirname(__file__)
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_PATH), autoescape=True
)


def render_template(name, **context):
    t = jinja_env.get_template(name)
    return Response(t.render(context), mimetype='text/html')


next_id = 1
contents = {}


def index():
    global contents
    return render_template('index.html', contents=contents)


def create():
    return render_template('create.html')


def store(req: Request):
    global next_id
    global contents
    contents[next_id] = {
        'id': next_id,
        'title': req.form['title'],
        'body': req.form['body'],
        'created_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }
    next_id += 1
    return redirect('/')


def edit(req, content_id):
    global contents
    if content_id not in contents:
        raise NotFound
    return render_template('edit.html', content=contents[content_id])


def update(req, content_id):
    global contents
    if content_id not in contents:
        raise NotFound

    contents[content_id].update({
        'title':
        req.form['title'],
        'body':
        req.form['body'],
        'updated_at':
        datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    })

    return redirect('/{}/edit'.format(content_id))


def destroy(content_id):
    global contents
    if content_id not in contents:
        raise NotFound

    contents.pop(content_id)

    return redirect('/')


app = Cezve()
app.route('/', store, methods=('POST', ))
app.route('/', index)
app.route('/create', create)
app.route('/<int:content_id>', update, methods=('POST', ))
app.route('/<int:content_id>', destroy, methods=('DELETE', ))
app.route('/<int:content_id>/edit', edit)
app.run()