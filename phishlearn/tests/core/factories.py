from datetime import timezone
import factory
from factory.django import DjangoModelFactory
from factory import Sequence, LazyAttribute, PostGenerationMethodCall, post_generation, SubFactory, lazy_attribute
from django.contrib.auth.models import User
from core.models import (
    UserProfile, Course, Quiz, Question, Choice, QuizAttempt,
    PhishingTemplate, PhishingTest, EmployeeGroup, LoginAttempt,
    Notification, QuizAssignment
)
from faker import Faker
faker = Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    email = LazyAttribute(lambda o: f"{o.username}@example.com")
    password = PostGenerationMethodCall('set_password', 'password123')

class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = SubFactory(UserFactory)
    user_type = "employee"

class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    title = Sequence(lambda n: f"Course {n}")
    description = factory.Faker("text")
    content = factory.Faker("text")
    created_by = SubFactory(UserFactory)
    is_published = True

class QuizFactory(DjangoModelFactory):
    class Meta:
        model = Quiz

    course = SubFactory(CourseFactory)
    title = factory.Faker("sentence")
    description = factory.Faker("text")

class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    quiz = SubFactory(QuizFactory)
    question_text = factory.Faker("sentence")

class ChoiceFactory(DjangoModelFactory):
    class Meta:
        model = Choice

    question = SubFactory(QuestionFactory)
    choice_text = factory.Faker("word")
    is_correct = factory.Faker("boolean")

class QuizAttemptFactory(DjangoModelFactory):
    class Meta:
        model = QuizAttempt

    user = SubFactory(UserFactory)
    quiz = SubFactory(QuizFactory)
    score = factory.Faker("random_int", min=0, max=100)

class PhishingTemplateFactory(DjangoModelFactory):
    class Meta:
        model = PhishingTemplate

    title = factory.Faker("sentence")
    subject = factory.Faker("sentence")
    content = factory.Faker("text")
    created_by = SubFactory(UserFactory)

# class PhishingTestFactory(DjangoModelFactory):
#     class Meta:
#         model = PhishingTest

#     template = SubFactory(PhishingTemplateFactory)
#     sent_by = SubFactory(UserFactory)
#     sent_to = SubFactory(UserFactory)
#     sent_at = factory.Faker("date_time_this_year")
#     clicked = factory.Faker("boolean")

#     @lazy_attribute
#     def clicked_at(self):
#         if self.clicked:
#             return faker.date_time_this_year()
#         return None

class EmployeeGroupFactory(DjangoModelFactory):
    class Meta:
        model = EmployeeGroup

    name = Sequence(lambda n: f"Group {n}")
    it_owner = SubFactory(UserFactory)

    @post_generation
    def employees(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for user in extracted:
                self.employees.add(user)

class LoginAttemptFactory(DjangoModelFactory):
    class Meta:
        model = LoginAttempt

    user = SubFactory(UserFactory)
    ip_address = factory.Faker("ipv4")
    timestamp = factory.Faker("date_time_this_year")
    success = factory.Faker("boolean")
    username = LazyAttribute(lambda o: o.user.username)
    browser_info = factory.Faker("user_agent")

class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    user = SubFactory(UserFactory)
    message = factory.Faker("sentence", nb_words=10)
    link = factory.Faker("uri_path")
    is_read = factory.Faker("boolean")
    created_at = factory.Faker("date_time_this_year")

class QuizAssignmentFactory(DjangoModelFactory):
    class Meta:
        model = QuizAssignment

    user = SubFactory(UserFactory)
    quiz = SubFactory(QuizFactory)
    assigned_date = factory.Faker("date_time_this_year")
    due_date = factory.Faker("future_datetime", end_date="+30d")
    status = factory.Iterator(['pending', 'completed', 'overdue'])
