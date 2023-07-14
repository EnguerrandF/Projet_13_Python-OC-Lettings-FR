from app_lettings import models

from django.test import Client
import pytest


pytestmark = pytest.mark.django_db


@pytest.fixture
def lettings_fixture():
    data_address = models.Address.objects.create(
        number=999,
        street='RUE du TEST',
        city='VILLAGETEST',
        state='FRANCE',
        zip_code=11540,
        country_iso_code='FR'
    )

    models.Letting.objects.create(
        title='TEST LETTING TITLE',
        address=data_address
    )

    yield


def test_lettings(lettings_fixture):
    client = Client()
    response = client.get('/lettings/')
    data_html = response.content.decode('utf-8')

    assert 'TEST LETTING TITLE' in data_html


def test_lettings_details(lettings_fixture):
    client = Client()
    response = client.get('/lettings/1/')
    data_html = response.content.decode('utf-8')

    assert '999' in data_html
    assert 'RUE du TEST' in data_html
    assert 'VILLAGETEST' in data_html
    assert 'FRANCE' in data_html
    assert '11540' in data_html
    assert 'FR' in data_html
