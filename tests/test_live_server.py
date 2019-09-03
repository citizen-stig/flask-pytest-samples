from flask import url_for
import requests


from demo_app import models


def test_list_categories(live_server, category_factory):
    categories = category_factory.create_batch(5)

    assert models.Category.query.count() == 5

    url = url_for('blog.list_categories', _external=True)

    response_1 = requests.get(url)

    assert response_1.status_code == 200
    data_1 = response_1.content.decode('utf-8')
    for category in categories:
        assert category.name in data_1

    assert models.Category.query.count() == 5

    response_2 = requests.get(url)

    assert response_2.status_code == 200
    data_2 = response_2.content.decode('utf-8')
    for category in categories:
        assert category.name in data_2
