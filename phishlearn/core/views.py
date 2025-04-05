from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import (
    UserProfile,
    Course,
    Quiz,
    Question,
    Choice,
    QuizAttempt,
    PhishingTemplate,
    PhishingTest,
    EmployeeGroup
)
import requests
from django.conf import settings

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create a UserProfile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
    
    if user_profile.user_type == 'employee':
        courses = Course.objects.all()
        quiz_attempts = QuizAttempt.objects.filter(user=request.user)
        phishing_tests = PhishingTest.objects.filter(sent_to=request.user)
        
        context = {
            'courses': courses,
            'quiz_attempts': quiz_attempts,
            'phishing_tests': phishing_tests,
        }
        return render(request, 'core/employee_dashboard.html', context)
    
    elif user_profile.user_type == 'it_owner':
        employee_groups = EmployeeGroup.objects.filter(it_owner=request.user)
        phishing_templates = PhishingTemplate.objects.all()
        sent_tests = PhishingTest.objects.filter(sent_by=request.user)
        
        context = {
            'employee_groups': employee_groups,
            'phishing_templates': phishing_templates,
            'sent_tests': sent_tests,
        }
        return render(request, 'core/it_owner_dashboard.html', context)
    
    else:  # site_admin
        users = User.objects.all()
        courses = Course.objects.all()
        phishing_templates = PhishingTemplate.objects.all()
        
        context = {
            'users': users,
            'courses': courses,
            'phishing_templates': phishing_templates,
        }
        return render(request, 'core/admin_dashboard.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quizzes = Quiz.objects.filter(course=course)
    
    context = {
        'course': course,
        'quizzes': quizzes,
    }
    return render(request, 'core/course_detail.html', context)

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    
    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        
        for question in questions:
            selected_choice = request.POST.get(f'question_{question.id}')
            if selected_choice:
                choice = Choice.objects.get(id=selected_choice)
                if choice.is_correct:
                    score += 1
        
        # Calculate percentage score
        percentage_score = (score / total_questions) * 100
        
        # Save quiz attempt
        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=percentage_score
        )
        
        messages.success(request, f'Quiz completed! Your score: {percentage_score}%')
        return redirect('dashboard')
    
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'core/take_quiz.html', context)

@login_required
def send_phishing_test(request):
    if not request.user.userprofile.user_type == 'it_owner':
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')
    
    if request.method == 'POST':
        template_id = request.POST.get('template')
        employee_ids = request.POST.getlist('employees')
        
        template = get_object_or_404(PhishingTemplate, id=template_id)
        
        for employee_id in employee_ids:
            employee = get_object_or_404(User, id=employee_id)
            PhishingTest.objects.create(
                template=template,
                sent_by=request.user,
                sent_to=employee,
                sent_at=timezone.now()
            )
        
        messages.success(request, 'Phishing test emails sent successfully')
        return redirect('dashboard')
    
    templates = PhishingTemplate.objects.all()
    employee_groups = EmployeeGroup.objects.filter(it_owner=request.user)
    
    context = {
        'templates': templates,
        'employee_groups': employee_groups,
    }
    return render(request, 'core/send_phishing_test.html', context)

@login_required
def manage_employees(request):
    if not request.user.userprofile.user_type == 'it_owner':
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')
    
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        employee_emails = request.POST.get('employee_emails').split(',')
        
        group = EmployeeGroup.objects.create(
            name=group_name,
            it_owner=request.user
        )
        
        for email in employee_emails:
            email = email.strip()
            try:
                employee = User.objects.get(email=email)
                group.employees.add(employee)
            except User.DoesNotExist:
                messages.warning(request, f'User with email {email} not found')
        
        messages.success(request, 'Employee group created successfully')
        return redirect('dashboard')
    
    groups = EmployeeGroup.objects.filter(it_owner=request.user)
    context = {'groups': groups}
    return render(request, 'core/manage_employees.html', context)

@login_required
def manage_courses(request):
    if not request.user.userprofile.user_type == 'site_admin':
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        
        Course.objects.create(
            title=title,
            description=description,
            content=content,
            created_by=request.user
        )
        
        messages.success(request, 'Course created successfully')
        return redirect('dashboard')
    
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'core/manage_courses.html', context)

@login_required
def manage_templates(request):
    if not request.user.userprofile.user_type == 'site_admin':
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        
        PhishingTemplate.objects.create(
            title=title,
            subject=subject,
            content=content,
            created_by=request.user
        )
        
        messages.success(request, 'Phishing template created successfully')
        return redirect('dashboard')
    
    templates = PhishingTemplate.objects.all()
    context = {'templates': templates}
    return render(request, 'core/manage_templates.html', context)

@login_required
def login_dashboard(request):
    # Fetch login attempts from Supabase
    url = f"{settings.SUPABASE_URL}/rest/v1/core_loginattempt"
    headers = {
    "apikey": settings.SUPABASE_KEY,
    "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    login_attempts = response.json() if response.status_code == 200 else []

    return render(request, 'core/login_dashboard.html', {'login_attempts': login_attempts})
