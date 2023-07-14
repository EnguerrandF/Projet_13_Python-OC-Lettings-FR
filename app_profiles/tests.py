from app_profiles.models import Profile
from django.contrib.auth.models import User

from django.test import Client
import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def profile_fixture():
    data_user = User.objects.create(
        username='TESTUSER',
        password='123456',
        first_name='TEST1',
        last_name='TEST2',
        email='test@email.com'
    )
    Profile.objects.create(
        user=data_user,
        favorite_city='TEST CITY'
    )

    yield


def test_profiles(profile_fixture):
    client = Client()
    response = client.get('/profiles/')
    data_html = response.content.decode('utf-8')

    assert 'TESTUSER' in data_html


def test_profiles_details(profile_fixture):
    client = Client()
    response = client.get('/profiles/TESTUSER/')
    data_html = response.content.decode('utf-8')

    assert 'First name: TEST1' in data_html
    assert 'Last name: TEST2' in data_html
    assert 'Email: test@email.com' in data_html
    assert 'Favorite city: TEST CITY' in data_html
