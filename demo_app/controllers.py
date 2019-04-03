from flask import Blueprint, redirect, url_for

from . import models

blog = Blueprint('blog', __name__)


@blog.route('/')
def hello_world():
    return 'Hello World!'


@blog.route('/categories')
def list_categories():
    return '<br/>'.join(str(x.id) + ': ' + x.name for x in models.Category.query)


@blog.route('/create-category/<string:name>')
def create_category(name):
    if name:
        category = models.Category(name=name)
        print('session: {}'.format(models.db.session))
        models.db.session.add(category)
        models.db.session.commit()
        return redirect(url_for('blog.list_categories'))
    return 'Please specify name'

