from flask import Blueprint

blog = Blueprint('blog', __name__)


@blog.route('/')
def hello_world():
    return 'Hello World!'
