import pytest
import os
import sys
import django
from django.conf import settings
from django.contrib.auth import get_user_model

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phishlearn.settings')
django.setup()

@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

@pytest.fixture
def client():
    from django.test import Client
    return Client()

@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='testpass123')
    return client 