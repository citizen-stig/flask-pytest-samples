from flask import url_for


from demo_app import models


def test_index(client):
    response = client.get(url_for('blog.hello_world'))

    assert response.status_code == 200
    assert response.data == b'Hello World!'


def test_list_categories_emtpy(client):
    response = client.get(url_for('blog.list_categories'))
    assert response.status_code == 200
    assert response.data == b''


def test_list_category_one_presented(client, category_factory):
    category = category_factory()

    response = client.get(url_for('blog.list_categories'))
    assert response.status_code == 200
    assert response.data == '{}: {}'.format(category.id, category.name).encode('utf-8')


def test_create_one_category(client, db_session):
    first_list_response = client.get(url_for('blog.list_categories'))
    assert first_list_response.status_code == 200
    assert first_list_response.data == b''

    name = 'my_name'
    create_response = client.get(url_for('blog.create_category', name=name))

    assert create_response.status_code == 302
    assert create_response.location == 'http://localhost/categories'

    second_list_response = client.get(url_for('blog.list_categories'))
    assert second_list_response.status_code == 200
    # assert second_list_response.data == b'1: my_name'


def test_create_two_categories(client, db_session):
    first_list_response = client.get(url_for('blog.list_categories'))
    assert first_list_response.status_code == 200
    assert first_list_response.data == b''

    names = ['юникод', '123']
    for name in names:
        create_response = client.get(url_for('blog.create_category', name=name))
        assert create_response.status_code == 302
        assert create_response.location == 'http://localhost/categories'

    assert models.Category.query.count() == 2

    second_list_response = client.get(url_for('blog.list_categories'))
    assert second_list_response.status_code == 200
    # assert second_list_response.data == b'2: \xd1\x8e\xd0\xbd\xd0\xb8\xd0\xba\xd0\xbe\xd0\xb4<br/>3: 123'


def test_list_posts(client, db_session, category_factory, post_factory):

    category = category_factory()
    url = url_for('blog.list_posts', category_name=category.name)
    post1 = post_factory(category=category)
    post2 = post_factory(category=category)
    post3 = post_factory()

    response = client.get(url)

    assert response.status_code == 200
    data = response.data.decode('utf-8')
    assert post1.title in data
    assert post2.title in data
    assert post3.title not in data

