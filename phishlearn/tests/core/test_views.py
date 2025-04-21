import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Course, Quiz, QuizAttempt, Notification, QuizAssignment
from tests.core.factories import (
    UserFactory, UserProfileFactory, CourseFactory, QuizFactory,
    QuestionFactory, ChoiceFactory, QuizAttemptFactory, EmployeeGroupFactory,
    NotificationFactory
)
from django.db.models.signals import post_save
from core.models import create_user_profile

@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert "Welcome" in response.content.decode() or "Home" in response.content.decode()

@pytest.mark.django_db
def test_dashboard_employee(client):
    user = UserFactory()
    # UserProfileFactory(user=user, user_type="employee")
    client.force_login(user)
    response = client.get(reverse("dashboard"))
    assert response.status_code == 200
    assert any("employee_dashboard" in t.name for t in response.templates)

@pytest.mark.django_db
def test_dashboard_it_owner(client):

    post_save.disconnect(receiver=create_user_profile, sender=User)

    user = UserFactory()
    UserProfileFactory(user=user, user_type="it_owner")
    client.force_login(user)
    response = client.get(reverse("dashboard"))
    assert response.status_code == 200
    assert any("it_owner_dashboard" in t.name for t in response.templates)

@pytest.mark.django_db
def test_course_detail(client):
    user = UserFactory()
    course = CourseFactory(created_by=user)
    client.force_login(user)
    response = client.get(reverse("course_detail", args=[course.id]))
    assert response.status_code == 200
    assert course.title in response.content.decode()

@pytest.mark.django_db
def test_take_quiz_correct_flow(client):

    post_save.disconnect(receiver=create_user_profile, sender=User)

    user = UserFactory()
    UserProfileFactory(user=user, user_type="employee")
    client.force_login(user)
    course = CourseFactory(created_by=user)
    quiz = QuizFactory(course=course)
    question = QuestionFactory(quiz=quiz)
    correct_choice = ChoiceFactory(question=question, is_correct=True)

    data = {
        f"question_{question.id}": correct_choice.id
    }
    response = client.post(reverse("take_quiz", args=[quiz.id]), data, follow=True)
    assert response.status_code == 200
    assert QuizAttempt.objects.filter(user=user, quiz=quiz).exists()
    assert Notification.objects.filter(user=user, message__icontains=quiz.title).exists()

@pytest.mark.django_db
def test_create_employee(client):
    admin = UserFactory(is_staff=True)
    client.force_login(admin)

    response = client.post(reverse("create_employee"), {
        "email": "test@example.com",
        "password": "securepassword123",
        "groups": []
    })

    assert response.status_code in (200, 302)
    assert User.objects.filter(email="test@example.com").exists()



@pytest.mark.django_db
def test_group_crud(client):

    post_save.disconnect(receiver=create_user_profile, sender=User)

    owner = UserFactory()
    UserProfileFactory(user=owner, user_type="it_owner") 
    client.force_login(owner)

    # Create group
    response = client.post(reverse("create_group"), {
        "name": "Red Team",
        "employee_emails": ""
    }, follow=True)

    print("Hello world")
    assert response.status_code == 200
    assert "Group created successfully" in response.content.decode()

    # List groups
    response = client.get(reverse("group_list"))
    assert response.status_code == 200
    assert "Red Team" in response.content.decode()

# Add more tests as needed for edge cases (wrong permissions, blank fields, etc.)
