import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import (
    Course, Quiz, QuizAttempt, Notification, QuizAssignment, PhishingTemplate, 
    
)
from tests.core.factories import (
    UserFactory, UserProfileFactory, CourseFactory, QuizFactory,
    QuestionFactory, ChoiceFactory, QuizAttemptFactory, EmployeeGroupFactory,
    NotificationFactory, PhishingTemplateFactory, QuizAssignmentFactory
)
from django.db.models.signals import post_save
from core.models import create_user_profile
from django.utils import timezone
from datetime import timedelta
from django.contrib.messages import get_messages
from unittest.mock import patch

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

# new here
@pytest.mark.django_db
def test_manage_courses_unauthorized(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="employee")  # 非 site_admin

    client.force_login(user)
    response = client.get(reverse("manage_courses"))

    # 应该被重定向
    assert response.status_code == 302
    assert response.url == reverse("dashboard")


@pytest.mark.django_db
def test_manage_courses_get_site_admin(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")

    CourseFactory.create_batch(3, created_by=user)

    client.force_login(user)
    response = client.get(reverse("manage_courses"))

    assert response.status_code == 200
    assert "core/manage_courses.html" in [t.name for t in response.templates]
    assert b"Course" in response.content


@pytest.mark.django_db
def test_manage_courses_post_create(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")

    client.force_login(user)

    data = {
        "title": "Test Course",
        "description": "This is a test course",
        "content": "Some content here"
    }
    response = client.post(reverse("manage_courses"), data, follow=True)

    assert response.status_code == 200
    assert Course.objects.filter(title="Test Course").exists()

    messages = list(get_messages(response.wsgi_request))
    assert any("Course created successfully" in str(m) for m in messages)


@pytest.mark.django_db
def test_manage_templates_unauthorized(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="employee")  # 非 site_admin

    client.force_login(user)
    response = client.get(reverse("manage_templates"))

    # 应该被重定向
    assert response.status_code == 302
    assert response.url == reverse("dashboard")


@pytest.mark.django_db
def test_manage_templates_get_site_admin(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")

    PhishingTemplateFactory.create_batch(2, created_by=user)

    client.force_login(user)
    response = client.get(reverse("manage_templates"))

    assert response.status_code == 200
    assert "core/manage_templates.html" in [t.name for t in response.templates]
    assert b"template" in response.content.lower()


@pytest.mark.django_db
def test_manage_templates_post_create(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")
    client.force_login(user)

    data = {
        "title": "Phish Test",
        "subject": "Watch out!",
        "content": "You've been hacked."
    }

    response = client.post(reverse("manage_templates"), data, follow=True)

    assert response.status_code == 200
    assert PhishingTemplate.objects.filter(title="Phish Test").exists()

    messages = list(get_messages(response.wsgi_request))
    assert any("Phishing template created successfully" in str(m) for m in messages)


@pytest.mark.django_db
def test_mark_all_read(client):
    user = UserFactory()
    client.force_login(user)
    NotificationFactory.create_batch(3, user=user, is_read=False)
    response = client.get(reverse("mark_all_read"))
    assert response.status_code == 302
    assert Notification.objects.filter(user=user, is_read=True).count() == 3

@pytest.mark.django_db
def test_login_dashboard_unauthorized(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="employee")  # not it_owner / site_admin

    client.force_login(user)
    response = client.get(reverse("login_dashboard"), follow=True)

    assert response.status_code == 200
    assert b"Unauthorized access" in response.content


@pytest.mark.django_db
@patch("core.views.requests.get")
def test_login_dashboard_success(mock_get, client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"username": "alice", "ip": "1.2.3.4", "success": True}
    ]

    client.force_login(user)
    response = client.get(reverse("login_dashboard"))

    assert response.status_code == 200
    assert "core/login_dashboard.html" in [t.name for t in response.templates]
    assert b"alice" in response.content
    # assert b"1.2.3.4" in response.content


@pytest.mark.django_db
@patch("core.views.requests.get")
def test_login_dashboard_supabase_error(mock_get, client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")

    mock_get.return_value.status_code = 500

    client.force_login(user)
    response = client.get(reverse("login_dashboard"))

    assert response.status_code == 200
    assert b"login_dashboard" in response.content
    # Should render empty login_attempts list gracefully
    assert "login_attempts" in response.context
    assert response.context["login_attempts"] == []

@pytest.mark.django_db
def test_assign_quiz_to_users(client):
    # 设置 IT Owner 用户
    it_owner = UserFactory()
    UserProfileFactory(user=it_owner, user_type="it_owner")
    client.force_login(it_owner)

    # 创建 Quiz 和两个员工用户
    quiz = QuizFactory()
    employee1 = UserFactory()
    UserProfileFactory(user=employee1, user_type="employee")
    employee2 = UserFactory()
    UserProfileFactory(user=employee2, user_type="employee")

    # 模拟表单提交
    url = reverse("assign_quiz_to_users")
    due_date = (timezone.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    response = client.post(url, {
        "quiz_id": quiz.id,
        "user_ids": [employee1.id, employee2.id],
        "due_date": due_date
    }, follow=True)

    # 检查状态码
    assert response.status_code == 200

    # 检查 QuizAssignment 是否创建成功
    assignments = QuizAssignment.objects.filter(quiz=quiz)
    assert assignments.count() == 2

    # 检查 Notification 是否发送
    assert Notification.objects.filter(user=employee1).exists()
    assert Notification.objects.filter(user=employee2).exists()

    # 检查提示信息
    assert "Quiz successfully assigned to 2 users" in response.content.decode()

@pytest.mark.django_db
def test_mark_all_read(client):
    # 创建用户并登录
    user = UserFactory()
    UserProfileFactory(user=user, user_type='employee')
    client.force_login(user)

    # 创建未读通知
    NotificationFactory.create_batch(3, user=user, is_read=False)
    NotificationFactory.create_batch(2, user=user, is_read=True)  # 已读通知不应受影响

    # 确保有 3 个未读通知
    assert Notification.objects.filter(user=user, is_read=False).count() == 3

    # 调用视图
    url = reverse("mark_all_read")
    response = client.get(url, follow=True)

    # 检查重定向成功
    assert response.status_code == 200
    assert response.redirect_chain[-1][0].endswith(reverse("dashboard"))

    # 所有通知应已被标记为已读
    assert Notification.objects.filter(user=user, is_read=False).count() == 0
    assert Notification.objects.filter(user=user, is_read=True).count() == 5

@pytest.mark.django_db
def test_courses_list_view_shows_correct_status(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="employee")
    client.force_login(user)

    # Setup: 3 courses: completed, in-progress, not-started
    completed_course = CourseFactory(is_published=True)
    in_progress_course = CourseFactory(is_published=True)
    not_started_course = CourseFactory(is_published=True)
    unpublished_course = CourseFactory(is_published=False)

    # Completed quiz attempt (>= 70)
    completed_quiz = QuizFactory(course=completed_course)
    QuizAttemptFactory(user=user, quiz=completed_quiz, score=85)

    # In-progress quiz attempt (< 70)
    in_progress_quiz = QuizFactory(course=in_progress_course)
    QuizAttemptFactory(user=user, quiz=in_progress_quiz, score=40)

    # No attempt for not_started_course
    QuizFactory(course=not_started_course)

    # Call view
    url = reverse("courses_list")
    response = client.get(url)

    assert response.status_code == 200
    assert "core/courses_list.html" in [t.name for t in response.templates]

    context_courses = response.context["courses"]
    # assert len(context_courses) == 3  # Only published courses

    # Check completion statuses
    status_map = {c["title"]: c["completion_status"] for c in context_courses}
    assert status_map[completed_course.title] == "completed"
    assert status_map[in_progress_course.title] == "in_progress"
    assert status_map[not_started_course.title] == "not_started"

@pytest.mark.django_db
def test_course_view_not_started(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type='employee')
    client.force_login(user)

    course = CourseFactory(is_published=True)
    QuizFactory(course=course)  # quiz exists but no attempt yet

    url = reverse("course_view", args=[course.id])
    response = client.get(url)

    assert response.status_code == 200
    # assert "not_started" in response.content.decode()


@pytest.mark.django_db
def test_course_view_in_progress(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type='employee')
    client.force_login(user)

    course = CourseFactory(is_published=True)
    quiz = QuizFactory(course=course)
    QuizAttemptFactory(user=user, quiz=quiz, score=30)  # below 70

    url = reverse("course_view", args=[course.id])
    response = client.get(url)

    assert response.status_code == 200
    # assert "in_progress" in response.content.decode()


@pytest.mark.django_db
def test_course_view_completed(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type='employee')
    client.force_login(user)

    course = CourseFactory(is_published=True)
    quiz = QuizFactory(course=course)
    QuizAttemptFactory(user=user, quiz=quiz, score=95)  # above 70

    url = reverse("course_view", args=[course.id])
    response = client.get(url)

    assert response.status_code == 200
    assert "completed" in response.content.decode()


@pytest.mark.django_db
def test_course_mark_complete(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type='employee')
    client.force_login(user)

    course = CourseFactory(is_published=True)
    QuizFactory(course=course)

    url = reverse("course_view", args=[course.id])
    response = client.post(url, {"action": "complete"}, follow=True)

    assert response.status_code == 200
    assert QuizAttempt.objects.filter(user=user, quiz__course=course).exists()
    assert Notification.objects.filter(user=user, message__contains="completed the course").exists()


@pytest.mark.django_db
def test_course_mark_in_progress(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type='employee')
    client.force_login(user)

    course = CourseFactory(is_published=True)
    QuizFactory(course=course)

    url = reverse("course_view", args=[course.id])
    response = client.post(url, {"action": "in_progress"}, follow=True)

    assert response.status_code == 200
    attempts = QuizAttempt.objects.filter(user=user, quiz__course=course)
    assert attempts.exists()
    assert any(a.score == 10 for a in attempts)


@pytest.mark.django_db
def test_my_profile_view_authenticated(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type='employee')

    client.force_login(user)
    url = reverse("my_profile")
    response = client.get(url)

    assert response.status_code == 200
    assert "Profile" in response.content.decode() or "profile" in response.template_name[0]


@pytest.mark.django_db
def test_my_profile_view_unauthenticated(client):
    url = reverse("my_profile")
    response = client.get(url)

    # Should redirect to login
    assert response.status_code == 302
    assert "/accounts/login/" in response.url

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from tests.core.factories import UserFactory, UserProfileFactory

User = get_user_model()


@pytest.mark.django_db
def test_change_password_success(client):
    user = UserFactory()
    user.set_password("old_password")
    user.save()
    UserProfileFactory(user=user)

    client.force_login(user)

    response = client.post(reverse("change_password"), {
        "current_password": "old_password",
        "new_password": "new_secure_pass123",
        "confirm_password": "new_secure_pass123"
    }, follow=True)

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password("new_secure_pass123")
    assert "Password changed successfully" in response.content.decode()


@pytest.mark.django_db
def test_change_password_wrong_current(client):
    user = UserFactory()
    user.set_password("correct_password")
    user.save()
    UserProfileFactory(user=user)

    client.force_login(user)

    response = client.post(reverse("change_password"), {
        "current_password": "wrong_password",
        "new_password": "new_secure_pass123",
        "confirm_password": "new_secure_pass123"
    }, follow=True)

    assert response.status_code == 200
    assert "Current password is incorrect" in response.content.decode()


@pytest.mark.django_db
def test_change_password_mismatch(client):
    user = UserFactory()
    user.set_password("old_password")
    user.save()
    UserProfileFactory(user=user)

    client.force_login(user)

    response = client.post(reverse("change_password"), {
        "current_password": "old_password",
        "new_password": "new_secure_pass123",
        "confirm_password": "not_matching"
    }, follow=True)

    assert response.status_code == 200
    assert "New passwords do not match" in response.content.decode()


@pytest.mark.django_db
def test_change_password_unauthenticated(client):
    response = client.post(reverse("change_password"), {
        "current_password": "doesntmatter",
        "new_password": "anything",
        "confirm_password": "anything"
    })

    # Should redirect to login
    assert response.status_code == 302
    assert "/accounts/login/" in response.url


@pytest.mark.django_db
def test_reset_api_key_success(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")
    client.force_login(user)

    with patch("core.views.reset_api_key") as mock_reset:
        mock_reset.return_value = {"success": True, "data": "new_key_123"}

        response = client.post(reverse("reset_api_key"), follow=True)
        assert response.status_code == 200
        assert "new_key_123" in response.content.decode()

        messages = list(get_messages(response.wsgi_request))
        assert any("API Key Reset" in str(m) for m in messages)


@pytest.mark.django_db
def test_reset_api_key_failure(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")
    client.force_login(user)

    with patch("core.views.reset_api_key") as mock_reset:
        mock_reset.return_value = {"success": False}

        response = client.post(reverse("reset_api_key"), follow=True)
        assert response.status_code == 200

        messages = list(get_messages(response.wsgi_request))
        assert any("Failed to reset API key" in str(m) for m in messages)


@pytest.mark.django_db
def test_reset_api_key_get_request(client):
    user = UserFactory()
    UserProfileFactory(user=user, user_type="site_admin")
    client.force_login(user)

    response = client.get(reverse("reset_api_key"))
    assert response.status_code == 200
    assert "API Key" in response.content.decode() or "Reset" in response.content.decode()