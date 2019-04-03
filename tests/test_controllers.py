from flask import url_for


def test_index(client):
    response = client.get(url_for('blog.hello_world'))

    assert response.status_code == 200
    assert response.data == b'Hello World!'


def test_list_categories_emtpy(client):
    response = client.get(url_for('blog.list_categories'))
    assert response.status_code == 200
    assert response.data == b''


def test_create_one_category(client):
    first_list_response = client.get(url_for('blog.list_categories'))
    assert first_list_response.status_code == 200
    assert first_list_response.data == b''

    name = 'my_name'
    create_response = client.get(url_for('blog.create_category', name=name))

    assert create_response.status_code == 302
    assert create_response.location == 'http://localhost/categories'

    second_list_response = client.get(url_for('blog.list_categories'))
    assert second_list_response.status_code == 200
    assert second_list_response.data == b'1: my_name'


# def test_create_two_categories(client):
#     first_list_response = client.get(url_for('blog.list_categories'))
#     assert first_list_response.status_code == 200
#     assert first_list_response.data == b''
#
#     names = ['юникод', '123']
#     for name in names:
#         create_response = client.get(url_for('blog.create_category', name=name))
#         assert create_response.status_code == 302
#         assert create_response.location == 'http://localhost/categories'
#
#     second_list_response = client.get(url_for('blog.list_categories'))
#     assert second_list_response.status_code == 200
#     assert second_list_response.data == b'1: my_name'
