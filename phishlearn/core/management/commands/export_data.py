from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Course, PhishingTemplate, 
    UserProfile, Quiz, Question, 
    Choice, QuizAttempt, PhishingTest, 
    EmployeeGroup, TrainingModule, 
    Notification, QuizAssignment
)
import json
from django.core.serializers import serialize

class Command(BaseCommand):
    help = 'Export all data to JSON file'

    def handle(self, *args, **kwargs):
        data = {
            'users': json.loads(serialize('json', User.objects.all())),
            'user_profiles': json.loads(serialize('json', UserProfile.objects.all())),
            'courses': json.loads(serialize('json', Course.objects.all())),
            'phishing_templates': json.loads(serialize('json', PhishingTemplate.objects.all())),
            'quizzes': json.loads(serialize('json', Quiz.objects.all())),
            'questions': json.loads(serialize('json', Question.objects.all())),
            'choices': json.loads(serialize('json', Choice.objects.all())),
            'quiz_attempts': json.loads(serialize('json', QuizAttempt.objects.all())),
            'phishing_tests': json.loads(serialize('json', PhishingTest.objects.all())),
            'employee_groups': json.loads(serialize('json', EmployeeGroup.objects.all())),
            'training_modules': json.loads(serialize('json', TrainingModule.objects.all())),
            'notifications': json.loads(serialize('json', Notification.objects.all())),
            'quiz_assignments': json.loads(serialize('json', QuizAssignment.objects.all())),
        }
        
        with open('db_backup.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        self.stdout.write(self.style.SUCCESS('Successfully exported data')) 