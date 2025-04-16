import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
import pytest_timeout

@pytest.fixture
def client():
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

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_home_view_accessible(client):
    """Test that home view is accessible to all users"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.content is not None

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_connection_check_view_accessible(client):
    """Test that connection check view is accessible to all users"""
    response = client.get('/connection/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)  # Check if response is JSON
    # Check for expected keys without requiring specific values
    assert 'database' in data
    assert 'supabase_client' in data

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_login_view_get(client):
    """Test login view GET request"""
    response = client.get('/accounts/login/')
    assert response.status_code == 200
    # Check for form elements instead of specific context
    content = response.content.decode()
    assert 'username' in content.lower()
    assert 'password' in content.lower()

@pytest.mark.django_db
@pytest.mark.timeout(15)
def test_login_view_post_success(client, user):
    """Test successful login"""
    response = client.post('/accounts/login/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.status_code == 302  # Redirect after successful login
    assert response.url == '/dashboard/'

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_login_view_post_failure(client):
    """Test failed login"""
    response = client.post('/accounts/login/', {
        'username': 'wronguser',
        'password': 'wrongpass'
    })
    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == "Invalid credentials. Please try again."

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_my_profile_view_requires_auth(client):
    """Test that my_profile view requires authentication"""
    response = client.get('/my-profile/')
    assert response.status_code == 302  # Redirect to login page
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_my_profile_view_accessible_when_authenticated(authenticated_client):
    """Test that my_profile view is accessible when authenticated"""
    response = authenticated_client.get('/my-profile/')
    assert response.status_code == 200
    assert 'user' in response.context

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_change_password_view_requires_auth(client):
    """Test that change_password view requires authentication"""
    response = client.get('/change-password/')
    assert response.status_code == 302  # Redirect to login page
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
@pytest.mark.timeout(15)
def test_change_password_success(authenticated_client, user):
    """Test successful password change"""
    response = authenticated_client.post('/change-password/', {
        'current_password': 'testpass123',
        'new_password': 'newpass123',
        'confirm_password': 'newpass123'
    })
    assert response.status_code == 302  # Redirect after successful change
    assert response.url == '/my-profile/'
    
    # Verify password was changed
    user.refresh_from_db()
    assert user.check_password('newpass123')

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_change_password_wrong_current(authenticated_client):
    """Test password change with wrong current password"""
    response = authenticated_client.post('/change-password/', {
        'current_password': 'wrongpass',
        'new_password': 'newpass123',
        'confirm_password': 'newpass123'
    })
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Current password is incorrect'

@pytest.mark.django_db
@pytest.mark.timeout(10)
def test_change_password_mismatch(authenticated_client):
    """Test password change with mismatched new passwords"""
    response = authenticated_client.post('/change-password/', {
        'current_password': 'testpass123',
        'new_password': 'newpass123',
        'confirm_password': 'differentpass'
    })
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'New passwords do not match'

@pytest.mark.django_db
@pytest.mark.timeout(15)
def test_change_password_keeps_session(authenticated_client, user):
    """Test that changing password doesn't log out the user"""
    response = authenticated_client.post('/change-password/', {
        'current_password': 'testpass123',
        'new_password': 'newpass123',
        'confirm_password': 'newpass123'
    })
    assert response.status_code == 302
    
    # Try accessing a protected page to verify still logged in
    response = authenticated_client.get('/my-profile/')
    assert response.status_code == 200
