import pytest
from django.contrib.auth.models import User
from core.models import (
    UserProfile, Course, Quiz, Question, Choice,
    QuizAttempt, PhishingTemplate, PhishingTest,
    EmployeeGroup, LoginAttempt, Notification, QuizAssignment
)
from django.utils import timezone
from tests.core.factories import (
    UserFactory, CourseFactory, QuizFactory,
    QuestionFactory, ChoiceFactory, QuizAttemptFactory,
    PhishingTemplateFactory, 
    EmployeeGroupFactory, NotificationFactory, QuizAssignmentFactory
)

pytestmark = pytest.mark.django_db

def test_user_profile_creation():
    user = UserFactory()
    profile = UserProfile.objects.get(user=user)
    assert profile.user == user

def test_course_str():
    course = CourseFactory(title="Cyber Security 101")
    assert str(course) == "Cyber Security 101"

def test_quiz_str():
    quiz = QuizFactory(title="Final Quiz")
    assert str(quiz) == f"{quiz.course.title} - Final Quiz"

def test_question_str():
    question = QuestionFactory(question_text="What is phishing?")
    assert str(question) == "What is phishing?"

def test_choice_str():
    choice = ChoiceFactory(choice_text="Correct Answer")
    assert str(choice) == "Correct Answer"

def test_quiz_attempt_str():
    attempt = QuizAttemptFactory(score=85)
    expected = f"{attempt.user.email} - {attempt.quiz.title} - 85"
    assert str(attempt) == expected

def test_phishing_template_str():
    template = PhishingTemplateFactory(title="Fake Email")
    assert str(template) == "Fake Email"

# def test_phishing_test_str():
#     test = PhishingTestFactory()
#     assert str(test) == f"{test.template.title} - {test.sent_to.email}"

def test_employee_group_str():
    group = EmployeeGroupFactory(name="Team A")
    assert str(group) == f"Team A - {group.it_owner.email}"

def test_login_attempt_str():
    attempt = LoginAttempt.objects.create(
        user=UserFactory(),
        ip_address="127.0.0.1",
        timestamp=timezone.now(),
        success=True,
        username="testuser",
        browser_info="Chrome"
    )
    assert str(attempt).startswith(str(attempt.user))

def test_notification_str():
    note = NotificationFactory(message="You have a new quiz")
    assert note.message in str(note)

def test_quiz_assignment_str():
    assignment = QuizAssignmentFactory()
    expected = f"{assignment.user.username} - {assignment.quiz.title}"
    assert str(assignment) == expected
