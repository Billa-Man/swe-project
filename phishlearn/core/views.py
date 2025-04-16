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
    EmployeeGroup,
    Notification, 
    QuizAssignment
)
import requests
from django.conf import settings
from django.urls import reverse


from .forms import EmployeeCreateForm, GroupCreateForm
from .models import EmployeeGroup, UserProfile
from django.db.models import Q
from django.core.paginator import Paginator
import logging

from .gophish_api import create_campaign, get_campaigns, get_campaign_status

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if user_profile.user_type == 'employee':
        courses = Course.objects.all()
        quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')
        phishing_tests = PhishingTest.objects.filter(sent_to=request.user)
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notification_count = notifications.count()
        
        # Get assigned quizzes that haven't been attempted yet
        assigned_quizzes = QuizAssignment.objects.filter(
            user=request.user,
            status='pending'
        ).order_by('due_date')
        
        # Calculate course completion statistics
        all_courses = Course.objects.all()
        total_courses = all_courses.count()
        
        # Get unique courses that the user has completed or in progress
        completed_course_ids = set()
        in_progress_course_ids = set()
        
        for attempt in quiz_attempts:
            course_id = attempt.quiz.course.id
            if attempt.score >= 70:  # Consider a score of 70% or above as 'complete'
                completed_course_ids.add(course_id)
            elif course_id not in completed_course_ids:
                in_progress_course_ids.add(course_id)
        
        # Filter out completed course IDs from in_progress_course_ids
        in_progress_course_ids = in_progress_course_ids - completed_course_ids
        
        completed_count = len(completed_course_ids)
        in_progress_count = len(in_progress_course_ids)
        not_started_count = total_courses - completed_count - in_progress_count
        
        # Make sure all counts are non-negative
        not_started_count = max(0, not_started_count)
        
        context = {
            'courses': courses,
            'quiz_attempts': quiz_attempts,
            'phishing_tests': phishing_tests,
            'notifications': notifications,
            'notification_count': notification_count,
            'quiz_assignments': assigned_quizzes,
            'completed_count': completed_count,
            'in_progress_count': in_progress_count,
            'not_started_count': not_started_count,
            'total_courses': total_courses,
        }
        return render(request, 'core/employee_dashboard.html', context)

    elif user_profile.user_type == 'it_owner':
        employee_groups = EmployeeGroup.objects.filter(it_owner=request.user)
        phishing_templates = PhishingTemplate.objects.all()
        sent_tests = PhishingTest.objects.filter(sent_by=request.user)
        
        quizzes = Quiz.objects.all()
        employees = User.objects.filter(userprofile__user_type='employee')

        campaigns = get_campaigns()  # Fetch all campaigns
        
        context = {
            'employee_groups': employee_groups,
            'phishing_templates': phishing_templates,
            'sent_tests': sent_tests,
            'quizzes': quizzes,
            'employees': employees,
            'campaigns': campaigns,
        }
        
        return render(request, 'core/it_owner_dashboard.html', context)


    else:
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

        percentage_score = int((score / total_questions) * 100)

        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=percentage_score
        )

        QuizAssignment.objects.filter(
            user=request.user,
            quiz=quiz,
            status='pending'
        ).update(status='completed')

        Notification.objects.create(
            user=request.user,
            message=f"You've completed the quiz: {quiz.title} with a score of {percentage_score}%",
            link=reverse('course_detail', args=[quiz.course.id])
        )

        messages.success(request, f'Quiz completed! Your score: {percentage_score}%')
        return redirect('dashboard')

    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'core/take_quiz.html', context)

# @login_required
# def send_phishing_test(request):
#     if not request.user.userprofile.user_type == 'it_owner':
#         messages.error(request, 'Unauthorized access')
#         return redirect('dashboard')

#     if request.method == 'POST':
#         template_id = request.POST.get('template')
#         employee_ids = request.POST.getlist('employees')

#         template = get_object_or_404(PhishingTemplate, id=template_id)

#         for employee_id in employee_ids:
#             employee = get_object_or_404(User, id=employee_id)
#             PhishingTest.objects.create(
#                 template=template,
#                 sent_by=request.user,
#                 sent_to=employee,
#                 sent_at=timezone.now()
#             )

#         messages.success(request, 'Phishing test emails sent successfully')
#         return redirect('dashboard')

#     templates = PhishingTemplate.objects.all()
#     employee_groups = EmployeeGroup.objects.filter(it_owner=request.user)

#     context = {
#         'templates': templates,
#         'employee_groups': employee_groups,
#     }
#     return render(request, 'core/send_phishing_test.html', context)

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
def list_employees(request):
    logger.info("View list_employees() called")

    search_query = request.GET.get('q', '')
    group_filter = request.GET.get('group', '')

    employees = User.objects.filter(userprofile__user_type='employee', is_staff=False).distinct().order_by('id')

    
    if search_query:
        employees = employees.filter(
            Q(username__icontains=search_query)  |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    if group_filter:
        employees = employees.filter(employee_groups__id=group_filter)

    paginator = Paginator(employees.distinct(), 20)  # 每页显示10个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    groups = EmployeeGroup.objects.all()

    return render(request, 'core/employee_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'group_filter': group_filter,
        'groups': groups,
    })

    
@login_required
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password'])
            user.save()

            groups = form.cleaned_data['groups']
            for group in groups:
                group.employees.add(user)

            messages.success(request, 'Employee created successfully.')
            return redirect('manage_employees')
    else:
        form = EmployeeCreateForm()
    return render(request, 'core/create_employee.html', {'form': form})


@login_required
def delete_emplpoyee(request, employee_id):
    if not request.user.userprofile.user_type == 'it_owner':
        messages.error(request, 'Unauthorized access')
        return redirect('manage_employees') 
    
    user = get_object_or_404(User, id = employee_id, userprofile__user_type='employee', is_staff=False)
    user.delete()
    messages.success(request, "Employee deleted successfully.")
    return redirect('manage_employees')
    

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.it_owner = request.user
            group.save()

            email_list = form.cleaned_data['employee_emails'].split(',')
            for email in email_list:
                email = email.strip()
                try:
                    user = User.objects.get(email=email)
                    group.employees.add(user)
                except User.DoesNotExist:
                    messages.warning(request, f'User with email {email} not found')

            messages.success(request, 'Group created successfully.')
            return redirect('group_list')
    else:
        form = GroupCreateForm()
    return render(request, 'core/create_group.html', {'form': form})


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(EmployeeGroup, id=group_id, it_owner=request.user)

    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Group deleted successfully.')
        return redirect('group_list')

    messages.error(request, 'Invalid request method.')
    return redirect('group_detail', group_id=group.id)


@login_required
def group_list(request):
    groups = EmployeeGroup.objects.filter(it_owner=request.user)
    return render(request, 'core/group_list.html', {'groups': groups})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(EmployeeGroup, id=group_id, it_owner=request.user)
    employees = group.employees.all()
    return render(request, 'core/group_detail.html', {'group': group, 'employees': employees})


@login_required
def add_member_to_group(request, group_id):

    group = get_object_or_404(EmployeeGroup, id=group_id, it_owner=request.user)

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_staff=False)
            group.employees.add(user)
            messages.success(request, f"{email} added to group.")
        except User.DoesNotExist:
            messages.error(request, f"No user found with email {email}.")
        return redirect('group_detail', group_id=group.id)
    

@login_required
def remove_employee_from_group(request, group_id, employee_id):
    group = get_object_or_404(EmployeeGroup, id=group_id, it_owner=request.user)
    user = get_object_or_404(User, id=employee_id, is_staff=False)

    if user in group.employees.all():
        group.employees.remove(user)
        messages.success(request, f"{user.email} has been removed from the group.")
    else:
        messages.warning(request, f"{user.email} is not in this group.")

    return redirect('group_detail', group_id=group.id)


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
    # Check if user is IT owner or site admin
    if not request.user.userprofile.user_type in ['it_owner', 'site_admin']:
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')

    url = f"{settings.SUPABASE_URL}/rest/v1/core_loginattempt"
    headers = {
        "apikey": settings.SUPABASE_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    login_attempts = response.json() if response.status_code == 200 else []

    return render(request, 'core/login_dashboard.html', {'login_attempts': login_attempts})


@login_required
def assign_quiz_to_users(request):
    if not request.user.userprofile.user_type in ['it_owner', 'site_admin']:
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')
    
    if request.method == 'POST':
        quiz_id = request.POST.get('quiz_id')
        user_ids = request.POST.getlist('user_ids')
        due_date_str = request.POST.get('due_date')
        
        # Parse due date or use default (7 days)
        if due_date_str:
            due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d')
            due_date = timezone.make_aware(due_date) 
        else:
            due_date = timezone.now() + timezone.timedelta(days=7)
            
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        for user_id in user_ids:
            user = get_object_or_404(User, id=user_id)
            
            # Create assignment
            QuizAssignment.objects.create(
                user=user,
                quiz=quiz,
                due_date=due_date,
            )
            
            # Create notification
            Notification.objects.create(
                user=user,
                message=f"New quiz assigned: {quiz.title}",
                link=reverse('take_quiz', args=[quiz.id])
            )
        
        messages.success(request, f'Quiz successfully assigned to {len(user_ids)} users')
        
    return redirect('dashboard')


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('dashboard')


@login_required
def courses_list(request):
    """View to display all available courses with completion status"""
    courses = Course.objects.filter(is_published=True)
    
    # Get all quiz attempts for this user
    quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')
    completed_course_ids = set()
    in_progress_course_ids = set()
    courses_with_status = []
    
    # Identify completed and in-progress courses based on quiz attempts
    for attempt in quiz_attempts:
        course_id = attempt.quiz.course.id
        if attempt.score >= 70:  # Consider a score of 70% or above as 'complete'
            completed_course_ids.add(course_id)
        elif course_id not in completed_course_ids:
            in_progress_course_ids.add(course_id)
    
    # For each course, determine completion status
    for course in courses:
        course_data = {
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'content': course.content,
        }
        
        if course.id in completed_course_ids:
            # Course is completed
            course_quiz_attempts = quiz_attempts.filter(
                quiz__course=course,
                score__gte=70
            )
            if course_quiz_attempts.exists():
                latest_attempt = course_quiz_attempts.latest('completed_at')
                course_data['completion_status'] = 'completed'
                course_data['completion_date'] = latest_attempt.completed_at
                course_data['score'] = latest_attempt.score
        elif course.id in in_progress_course_ids:
            # Course is in progress
            course_quiz_attempts = quiz_attempts.filter(
                quiz__course=course
            )
            if course_quiz_attempts.exists():
                latest_attempt = course_quiz_attempts.latest('completed_at')
                course_data['completion_status'] = 'in_progress'
                course_data['completion_date'] = latest_attempt.completed_at
                course_data['score'] = latest_attempt.score
        else:
            course_data['completion_status'] = 'not_started'
            course_data['completion_date'] = None
            course_data['score'] = None
        
        courses_with_status.append(course_data)
    
    context = {
        'courses': courses_with_status,
    }
    return render(request, 'core/courses_list.html', context)

@login_required
def course_view(request, course_id):
    """View to display a specific course and allow marking as complete"""
    course = get_object_or_404(Course, id=course_id)
    
    # Check if the user has completed quizzes for this course
    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user,
        quiz__course=course
    )
    
    if quiz_attempts.filter(score__gte=70).exists():
        # If there's at least one attempt with score ≥ 70%, consider as completed
        latest_attempt = quiz_attempts.filter(score__gte=70).latest('completed_at')
        completion_status = 'completed'
        completion_date = latest_attempt.completed_at
        score = latest_attempt.score
    elif quiz_attempts.exists():
        # If there are attempts but none with score ≥ 70%, consider as in progress
        latest_attempt = quiz_attempts.latest('completed_at')
        completion_status = 'in_progress'
        completion_date = latest_attempt.completed_at
        score = latest_attempt.score
    else:
        # If no attempts, consider as not started
        completion_status = 'not_started'
        completion_date = None
        score = None
    
    # Handle course completion requests
    if request.method == 'POST':
        action = request.POST.get('action')
        quizzes = Quiz.objects.filter(course=course)
        
        if action == 'complete':
            # If there are no quizzes for this course, create a dummy one
            if not quizzes.exists():
                quiz = Quiz.objects.create(
                    course=course,
                    title=f"{course.title} Quiz",
                    description=f"Quiz for {course.title}"
                )
                quizzes = [quiz]
            
            # Mark course as complete by creating a quiz attempt for each quiz
            for quiz in quizzes:
                QuizAttempt.objects.create(
                    user=request.user,
                    quiz=quiz,
                    score=100  # Default score for self-marked completion
                )
            
            Notification.objects.create(
                user=request.user,
                message=f"You've completed the course: {course.title}",
                link=reverse('course_view', args=[course.id])
            )
            messages.success(request, f'Course marked as complete')
            return redirect('course_view', course_id=course.id)
            
        elif action == 'in_progress':
            # Mark first quiz as started with a low score to indicate in progress
            if quizzes.exists():
                QuizAttempt.objects.create(
                    user=request.user,
                    quiz=quizzes.first(),
                    score=10  # Low score indicates in progress
                )
                completion_status = 'in_progress'
                completion_date = timezone.now()
                score = 10
            else:
                # If no quizzes exist, create one and mark it as in progress
                quiz = Quiz.objects.create(
                    course=course,
                    title=f"{course.title} Quiz",
                    description=f"Quiz for {course.title}"
                )
                QuizAttempt.objects.create(
                    user=request.user,
                    quiz=quiz,
                    score=10  # Low score indicates in progress
                )
                completion_status = 'in_progress'
                completion_date = timezone.now()
                score = 10
                
            messages.success(request, f'Course marked as in progress')
            return redirect('course_view', course_id=course.id)
    
    context = {
        'course': course,
        'completion_status': completion_status,
        'completion_date': completion_date,
        'score': score,
    }
    return render(request, 'core/course_view.html', context)

@login_required
def create_campaign_view(request):
    if request.method == 'POST':
        name = request.POST['campaign_name']
        sender_email = request.POST['sender_email']
        target_group = request.POST['target_group']
        email_template_id = request.POST['email_template']
        url = request.POST['url']

        campaign_response = create_campaign(name, sender_email, target_group, email_template_id, url)
        return render(request, 'campaign_created.html', {'campaign': campaign_response})
    return render(request, 'create_campaign.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .gophish_api import create_campaign, get_campaigns, get_email_templates, get_employee_groups

def send_phishing_test(request):
    # Get templates and groups for the form
    templates = get_email_templates()  # Implement this to fetch from GoPhish
    employee_groups = get_employee_groups()  # Implement this to fetch from GoPhish
    
    if request.method == 'POST':
        # Extract form data
        campaign_name = request.POST.get('campaign_name')
        sender_email = request.POST.get('sender_email')
        target_group = request.POST.get('target_group')
        email_template_id = request.POST.get('email_template_id')
        url = request.POST.get('url')
        
        # Create campaign in GoPhish
        response = create_campaign(
            name=campaign_name,
            sender_email=sender_email,
            target_group=target_group,
            email_template_id=email_template_id,
            url=url
        )
        
        if 'id' in response:
            messages.success(request, f"Campaign '{campaign_name}' created successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, f"Error creating campaign: {response.get('message', 'Unknown error')}")
    
    return render(request, 'core/send_phishing_test.html', {
        'templates': templates,
        'employee_groups': employee_groups,
    })

from django.http import JsonResponse
from .gophish_api import get_campaigns, get_campaign_status

def gophish_campaigns_api(request):
    campaigns = get_campaigns()
    return JsonResponse(campaigns, safe=False)

def gophish_template_preview_api(request, template_id):
    # This would need implementation based on how GoPhish provides template previews
    # You might need to fetch the template details from GoPhish
    # For now, returning a placeholder
    return JsonResponse({
        'name': 'Template Name',
        'html': '<p>Template HTML content would go here.</p>'
    })
