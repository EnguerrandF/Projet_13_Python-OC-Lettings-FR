from django.test import Client


def test_homepage():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200
