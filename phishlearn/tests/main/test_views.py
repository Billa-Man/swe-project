# tests/main/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from unittest.mock import patch
from core.models import LoginAttempt

@pytest.mark.django_db
def test_connection_check_view(client):
    response = client.get(reverse('connection_check'))
    assert response.status_code == 200
    assert 'database' in response.json()
    assert 'supabase_client' in response.json()


@pytest.mark.django_db
def test_login_view_success(client):
    user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    response = client.post(reverse('login_view'), data={
        'username': 'testuser',
        'password': 'password123'
    }, follow=True)

    assert response.status_code == 200
    assert response.wsgi_request.user.is_authenticated
    assert LoginAttempt.objects.filter(username='testuser', success=True).exists()


@pytest.mark.django_db
def test_login_view_failure(client):
    response = client.post(reverse('login_view'), data={
        'username': 'fakeuser',
        'password': 'wrongpass'
    }, follow=True)

    assert response.status_code == 200
    assert 'Invalid credentials' in response.content.decode()
    assert LoginAttempt.objects.filter(username='fakeuser', success=False).exists()


@pytest.mark.django_db
def test_login_redirect_for_admin(client):
    admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')

    response = client.post(reverse('login_view'), data={
        'username': 'admin',
        'password': 'adminpass'
    }, follow=True)

    assert response.status_code == 200
    assert "Admins must login via /admin/" in response.content.decode()


@pytest.mark.django_db
def test_login_get_form_display(client):
    response = client.get(reverse('login_view'))
    assert response.status_code == 200
    assert "<form" in response.content.decode()
