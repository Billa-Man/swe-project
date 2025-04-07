from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    USER_TYPES = (
        ('employee', 'Employee'),
        ('it_owner', 'IT Owner'),
        ('site_admin', 'Site Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='employee')
    organization = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.user_type}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)  # Add this line
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.score}"

class PhishingTemplate(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class PhishingTest(models.Model):
    template = models.ForeignKey(PhishingTemplate, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(User, related_name='sent_tests', on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User, related_name='received_tests', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)
    clicked = models.BooleanField(default=False)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.template.title} - {self.sent_to.email}"

class EmployeeGroup(models.Model):
    name = models.CharField(max_length=100)
    it_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    employees = models.ManyToManyField(User, related_name='employee_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.it_owner.email}"

class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    success = models.BooleanField()
    username = models.CharField(max_length=255, null=True)
    browser_info = models.TextField(null=True)

    def __str__(self):
        return f"{self.user} - {self.success} - {self.timestamp}"

class TrainingModule(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class ModuleCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.module.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}"
    
class QuizAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue')
    ], default='pending')
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"