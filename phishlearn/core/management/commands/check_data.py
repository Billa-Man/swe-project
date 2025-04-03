from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Course, PhishingTemplate, UserProfile, Quiz, Question, Choice, QuizAttempt, PhishingTest, EmployeeGroup

class Command(BaseCommand):
    help = 'Check imported data counts'

    def handle(self, *args, **kwargs):
        models = {
            'Users': User,
            'UserProfiles': UserProfile,
            'Courses': Course,
            'PhishingTemplates': PhishingTemplate,
            'Quizzes': Quiz,
            'Questions': Question,
            'Choices': Choice,
            'QuizAttempts': QuizAttempt,
            'PhishingTests': PhishingTest,
            'EmployeeGroups': EmployeeGroup,
        }
        
        for name, model in models.items():
            count = model.objects.count()
            self.stdout.write(f'{name}: {count} records') 