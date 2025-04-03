from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Course, PhishingTemplate, UserProfile, Quiz, Question, Choice, QuizAttempt, PhishingTest, EmployeeGroup
import json
from django.db import transaction

class Command(BaseCommand):
    help = 'Import data from JSON file'

    def handle(self, *args, **kwargs):
        try:
            with open('db_backup.json', 'r') as f:
                data = json.load(f)

            with transaction.atomic():
                # Import Users first
                for user_data in data['users']:
                    if not User.objects.filter(username=user_data['fields']['username']).exists():
                        User.objects.create_user(
                            username=user_data['fields']['username'],
                            email=user_data['fields']['email'],
                            password=user_data['fields']['password'],
                            is_staff=user_data['fields']['is_staff'],
                            is_superuser=user_data['fields']['is_superuser']
                        )

                # Import UserProfiles
                for profile in data['user_profiles']:
                    if not UserProfile.objects.filter(user_id=profile['fields']['user']).exists():
                        UserProfile.objects.create(
                            user_id=profile['fields']['user'],
                            user_type=profile['fields']['user_type'],
                            organization=profile['fields'].get('organization', '')
                        )

                # Import all other models in order
                self.import_model(Course, data.get('courses', []))
                self.import_model(PhishingTemplate, data.get('phishing_templates', []))
                self.import_model(Quiz, data.get('quizzes', []))
                self.import_model(Question, data.get('questions', []))
                self.import_model(Choice, data.get('choices', []))
                self.import_model(QuizAttempt, data.get('quiz_attempts', []))
                self.import_model(PhishingTest, data.get('phishing_tests', []))
                self.import_model(EmployeeGroup, data.get('employee_groups', []))

            self.stdout.write(self.style.SUCCESS('Successfully imported data'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))

    def import_model(self, model, data_list):
        for item in data_list:
            if not model.objects.filter(id=item['pk']).exists():
                model.objects.create(id=item['pk'], **item['fields']) 