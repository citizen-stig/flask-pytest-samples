import string
import random
from flask import Blueprint, redirect, url_for, render_template

from . import models

blog = Blueprint('blog', __name__)


@blog.route('/')
def hello_world():
    return 'Hello World!'


@blog.route('/categories')
def list_categories():
    print('list categories, models.Category.query.session:', models.Category.query.session)
    return '<br/>'.join(str(x.id) + ': ' + x.name for x in models.Category.query)


@blog.route('/create-category/<string:name>')
def create_category(name):
    if name:
        category = models.Category(name=name)
        print('create_category models.db.session: {}'.format(models.db.session))
        models.db.session.add(category)
        models.db.session.commit()
        return redirect(url_for('blog.list_categories'))
    return 'Please specify name'


ALPHABET = string.ascii_uppercase + string.digits + ' '


def rand_string(length, alphabet=ALPHABET):
    return ''.join(random.choice(alphabet) for _ in range(length))


@blog.route('/category/<string:category_name>/')
def list_posts(category_name):
    print('list posts, models.Category.query.session:', models.Category.query.session)
    category = models.Category.query \
        .filter(models.Category.name == category_name) \
        .first_or_404()
    return render_template('posts.html', category=category)


@blog.route('/category/<string:category_name>/<int:posts_number>')
def create_x_posts(category_name, posts_number):
    print('create posts, models.Category.query.session:', models.Category.query.session)
    category = models.Category.query \
        .filter(models.Category.name == category_name)\
        .first_or_404()
    print('create_category models.db.session: {}'.format(models.db.session))
    for x in range(posts_number):
        post = models.Post(
            title=rand_string(20),
            body=rand_string(180, alphabet=ALPHABET + '\n'),
            category=category,
        )
        models.db.session.add(post)
        models.db.session.commit()

    return redirect(url_for('blog.list_posts', category_name=category.name))
