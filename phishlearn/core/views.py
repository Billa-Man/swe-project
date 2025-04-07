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
    CourseCompletion,
    Notification, 
    QuizAssignment,
    CourseProgress,
    CourseAssignment
)
import requests
from django.conf import settings
from django.urls import reverse

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    try:
        user_profile = request.user.userprofile
        
        if user_profile.user_type == 'employee':
            # Get all published courses
            all_courses = Course.objects.filter(is_published=True)
            total_courses = all_courses.count()
            
            # Get completed courses
            completed_courses = CourseCompletion.objects.filter(user=request.user)
            completed_count = completed_courses.count()
            completed_course_ids = completed_courses.values_list('course_id', flat=True)
            
            # Get in-progress courses from CourseProgress model
            in_progress_courses = CourseProgress.objects.filter(
                user=request.user,
                course__in=all_courses
            ).exclude(course_id__in=completed_course_ids)
            in_progress_count = in_progress_courses.count()
            
            # Calculate not started count
            not_started_count = total_courses - completed_count - in_progress_count
            
            # Calculate progress percentage
            progress_percentage = int((completed_count / total_courses * 100) if total_courses > 0 else 0)
            
            # Get quiz attempts and phishing tests
            quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-completed_at')
            phishing_tests = PhishingTest.objects.filter(sent_to=request.user)
            
            # Get notifications
            notifications = Notification.objects.filter(user=request.user, is_read=False)
            notification_count = notifications.count()
            
            # Get assigned quizzes that haven't been attempted yet
            attempted_quiz_ids = quiz_attempts.values_list('quiz_id', flat=True)
            assigned_quizzes = QuizAssignment.objects.filter(
                user=request.user,
                status='pending'
            ).order_by('due_date')
            
            context = {
                'courses': all_courses,
                'quiz_attempts': quiz_attempts,
                'phishing_tests': phishing_tests,
                'completed_courses': completed_courses,
                'notifications': notifications,
                'notification_count': notification_count,
                'quiz_assignments': assigned_quizzes,
                'progress_percentage': progress_percentage,
                'completed_count': completed_count,
                'in_progress_count': in_progress_count,
                'not_started_count': not_started_count,
                'total_courses': total_courses
            }
            return render(request, 'core/employee_dashboard.html', context)

        elif user_profile.user_type == 'it_owner':
            # Get employee groups and templates
            employee_groups = EmployeeGroup.objects.filter(it_owner=request.user)
            phishing_templates = PhishingTemplate.objects.all()
            
            # Get only active employees with complete profiles
            employees = User.objects.filter(
                userprofile__user_type='employee',
                is_active=True
            ).select_related('userprofile').exclude(
                first_name='',
                last_name=''
            )
            
            # Calculate progress for each employee
            for employee in employees:
                total_courses = Course.objects.filter(is_published=True).count()
                completed_courses = CourseCompletion.objects.filter(user=employee).count()
                employee.progress = int((completed_courses / total_courses * 100) if total_courses > 0 else 0)
            
            # Get email campaign statistics
            phishing_tests = PhishingTest.objects.all()
            total_tests = phishing_tests.count()
            if total_tests > 0:
                opened_count = phishing_tests.filter(opened=True).count()
                clicked_count = phishing_tests.filter(clicked=True).count()
                bounced_count = phishing_tests.filter(bounced=True).count()
                
                open_rate = int((opened_count / total_tests) * 100)
                click_rate = int((clicked_count / total_tests) * 100)
                bounce_rate = int((bounced_count / total_tests) * 100)
            else:
                open_rate = click_rate = bounce_rate = 0
            
            # Get latest campaign date
            latest_campaign = phishing_tests.order_by('-sent_at').first()
            
            context = {
                'employee_groups': employee_groups,
                'phishing_templates': phishing_templates,
                'employees': employees,
                'open_rate': open_rate,
                'click_rate': click_rate,
                'bounce_rate': bounce_rate,
                'latest_campaign': latest_campaign
            }
            return render(request, 'core/it_owner_dashboard.html', context)
            
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return redirect('home')

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
def course_list(request):
    courses = Course.objects.filter(is_published=True).prefetch_related('coursecompletion_set')
    
    # Annotate courses with user's completion and progress status
    for course in courses:
        course.user_completion = course.coursecompletion_set.filter(user=request.user).first()
        course.user_progress = CourseProgress.objects.filter(user=request.user, course=course).first()
    
    context = {
        'courses': courses
    }
    return render(request, 'core/course_list.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    completion = CourseCompletion.objects.filter(user=request.user, course=course).first()
    progress = CourseProgress.objects.filter(user=request.user, course=course).first()
    quizzes = Quiz.objects.filter(course=course)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'complete' and not completion:
            # Calculate the average score from all related quizzes
            quiz_attempts = QuizAttempt.objects.filter(
                user=request.user,
                quiz__in=quizzes
            )
            
            if quiz_attempts.exists():
                average_score = sum(attempt.score for attempt in quiz_attempts) / quiz_attempts.count()
            else:
                average_score = 0
            
            completion = CourseCompletion.objects.create(
                user=request.user,
                course=course,
                score=average_score
            )
            
            # Remove in-progress status if exists
            if progress:
                progress.delete()
            
            messages.success(request, f'Congratulations! You have completed the {course.title} course.')
            
            # Create a notification
            Notification.objects.create(
                user=request.user,
                message=f"You've completed the course: {course.title}",
                link=reverse('course_detail', args=[course.id])
            )
        
        elif action == 'mark_in_progress' and not completion and not progress:
            # Mark the course as in progress
            CourseProgress.objects.create(
                user=request.user,
                course=course
            )
            
            messages.success(request, f'You have marked the {course.title} course as in progress.')
        
        return redirect('course_detail', course_id=course.id)
    
    context = {
        'course': course,
        'completion': completion,
        'progress': progress,
        'quizzes': quizzes
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

        # Update course completion if all quizzes are completed
        course = quiz.course
        all_course_quizzes = Quiz.objects.filter(course=course)
        user_quiz_attempts = QuizAttempt.objects.filter(
            user=request.user,
            quiz__in=all_course_quizzes
        ).values_list('quiz_id', flat=True)

        if set(user_quiz_attempts) == set(all_course_quizzes.values_list('id', flat=True)):
            # All quizzes completed, calculate average score
            average_score = QuizAttempt.objects.filter(
                user=request.user,
                quiz__in=all_course_quizzes
            ).aggregate(Avg('score'))['score__avg']

            CourseCompletion.objects.update_or_create(
                user=request.user,
                course=course,
                defaults={'score': round(average_score)}
            )

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
            # UserProfile.objects.create(user=user, user_type='employee')

            groups = form.cleaned_data['groups']
            for group in groups:
                group.employees.add(user)

            messages.success(request, 'Employee created successfully.')
            return redirect('list_employees')
    else:
        form = EmployeeCreateForm()
    return render(request, 'core/create_employee.html', {'form': form})

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
def manage_courses(request):
    if not request.user.userprofile.user_type == 'site_admin':
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'toggle_publish':
            course_id = request.POST.get('course_id')
            course = get_object_or_404(Course, id=course_id)
            course.is_published = not course.is_published
            course.save()
            status = 'published' if course.is_published else 'unpublished'
            messages.success(request, f'Course "{course.title}" has been {status}.')
            return redirect('manage_courses')
        
        # Handle course creation
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        is_published = request.POST.get('is_published') == 'on'

        Course.objects.create(
            title=title,
            description=description,
            content=content,
            created_by=request.user,
            is_published=is_published
        )

        messages.success(request, 'Course created successfully')
        return redirect('manage_courses')

    courses = Course.objects.all().order_by('-created_at')
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
        
        # Parse due date or use default (14 days)
        if due_date_str:
            due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d')
            due_date = timezone.make_aware(due_date) 
        else:
            due_date = timezone.now() + timezone.timedelta(days=14)
            
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
def module_list(request):
    modules = TrainingModule.objects.all().prefetch_related('modulecompletion_set')
    
    # Annotate modules with user's completion status
    for module in modules:
        module.user_completion = module.modulecompletion_set.filter(user=request.user).first()
    
    context = {
        'modules': modules
    }
    return render(request, 'core/module_list.html', context)

@login_required
def module_detail(request, module_id):
    module = get_object_or_404(TrainingModule, id=module_id)
    completion = ModuleCompletion.objects.filter(user=request.user, module=module).first()
    quizzes = Quiz.objects.filter(course__in=module.course_set.all())
    
    if request.method == 'POST' and not completion:
        # Calculate the average score from all related quizzes
        quiz_attempts = QuizAttempt.objects.filter(
            user=request.user,
            quiz__in=quizzes
        )
        
        if quiz_attempts.exists():
            average_score = sum(attempt.score for attempt in quiz_attempts) / quiz_attempts.count()
        else:
            average_score = 0
        
        completion = ModuleCompletion.objects.create(
            user=request.user,
            module=module,
            score=average_score
        )
        
        messages.success(request, f'Congratulations! You have completed the {module.title} module.')
        
        # Create a notification
        Notification.objects.create(
            user=request.user,
            message=f"You've completed the module: {module.title} with a score of {average_score}%",
            link=reverse('module_detail', args=[module.id])
        )
        
        return redirect('module_detail', module_id=module.id)
    
    context = {
        'module': module,
        'completion': completion,
        'quizzes': quizzes
    }
    return render(request, 'core/module_detail.html', context)

@login_required
def manage_course_assignments(request):
    if not request.user.userprofile.user_type in ['it_owner', 'site_admin']:
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'assign':
            course_id = request.POST.get('course_id')
            user_ids = request.POST.getlist('user_ids')
            due_date_str = request.POST.get('due_date')
            
            # Parse due date if provided
            due_date = None
            if due_date_str:
                due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d')
                due_date = timezone.make_aware(due_date)
            
            course = get_object_or_404(Course, id=course_id)
            
            for user_id in user_ids:
                user = get_object_or_404(User, id=user_id)
                
                # Create or update assignment
                CourseAssignment.objects.update_or_create(
                    user=user,
                    course=course,
                    defaults={
                        'assigned_by': request.user,
                        'due_date': due_date
                    }
                )
                
                # Create notification
                Notification.objects.create(
                    user=user,
                    message=f"New course assigned: {course.title}",
                    link=reverse('course_detail', args=[course.id])
                )
            
            messages.success(request, f'Course successfully assigned to {len(user_ids)} users')
            
        elif action == 'remove':
            assignment_id = request.POST.get('assignment_id')
            assignment = get_object_or_404(CourseAssignment, id=assignment_id)
            
            # Create notification about removal
            Notification.objects.create(
                user=assignment.user,
                message=f"Course assignment removed: {assignment.course.title}",
                link=reverse('course_list')
            )
            
            assignment.delete()
            messages.success(request, 'Course assignment removed successfully')
    
    # Get all employees
    employees = User.objects.filter(userprofile__user_type='employee')
    
    # Get all published courses
    courses = Course.objects.filter(is_published=True)
    
    # Get all course assignments
    assignments = CourseAssignment.objects.all().select_related('user', 'course', 'assigned_by')
    
    # Get employee groups for IT owners
    employee_groups = None
    if request.user.userprofile.user_type == 'it_owner':
        employee_groups = EmployeeGroup.objects.filter(it_owner=request.user)
    
    context = {
        'employees': employees,
        'courses': courses,
        'assignments': assignments,
        'employee_groups': employee_groups
    }
    
    return render(request, 'core/manage_course_assignments.html', context)

@login_required
def manage_quiz_assignments(request):
    if not request.user.userprofile.user_type in ['it_owner', 'site_admin']:
        messages.error(request, 'Unauthorized access')
        return redirect('dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'assign':
            quiz_id = request.POST.get('quiz_id')
            user_ids = request.POST.getlist('user_ids')
            due_date_str = request.POST.get('due_date')
            
            # Parse due date if provided
            due_date = None
            if due_date_str:
                due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d')
                due_date = timezone.make_aware(due_date)
            else:
                due_date = timezone.now() + timezone.timedelta(days=14)  # Default 14 days
            
            quiz = get_object_or_404(Quiz, id=quiz_id)
            
            for user_id in user_ids:
                user = get_object_or_404(User, id=user_id)
                
                # Create or update assignment
                QuizAssignment.objects.update_or_create(
                    user=user,
                    quiz=quiz,
                    defaults={
                        'due_date': due_date,
                        'status': 'pending'
                    }
                )
                
                # Create notification
                Notification.objects.create(
                    user=user,
                    message=f"New quiz assigned: {quiz.title}",
                    link=reverse('take_quiz', args=[quiz.id])
                )
            
            messages.success(request, f'Quiz successfully assigned to {len(user_ids)} users')
            
        elif action == 'remove':
            assignment_id = request.POST.get('assignment_id')
            assignment = get_object_or_404(QuizAssignment, id=assignment_id)
            
            # Create notification about removal
            Notification.objects.create(
                user=assignment.user,
                message=f"Quiz assignment removed: {assignment.quiz.title}",
                link=reverse('course_list')
            )
            
            assignment.delete()
            messages.success(request, 'Quiz assignment removed successfully')
    
    # Get all employees
    employees = User.objects.filter(userprofile__user_type='employee')
    
    # Get all quizzes from published courses
    quizzes = Quiz.objects.filter(course__is_published=True)
    
    # Get all quiz assignments
    assignments = QuizAssignment.objects.all().select_related('user', 'quiz')
    
    # Get employee groups for IT owners
    employee_groups = None
    if request.user.userprofile.user_type == 'it_owner':
        employee_groups = EmployeeGroup.objects.filter(it_owner=request.user)
    
    context = {
        'employees': employees,
        'quizzes': quizzes,
        'assignments': assignments,
        'employee_groups': employee_groups
    }
    
    return render(request, 'core/manage_quiz_assignments.html', context)