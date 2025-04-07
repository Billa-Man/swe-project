from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),  # optional: pick one
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('send-phishing-test/', views.send_phishing_test, name='send_phishing_test'),
    path('manage-employees/', views.manage_employees, name='manage_employees'),  # if you're using this view
    # or: path('manage-employees/', views.list_employees, name='manage_employees'),

    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('manage-templates/', views.manage_templates, name='manage_templates'),
    path('login-dashboard/', views.login_dashboard, name='login_dashboard'),  # only in HEAD
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),  # HEAD style
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),  # origin/main style
    path('manage-quiz-assignments/', views.manage_quiz_assignments, name='manage_quiz_assignments'),
    path('manage-course-assignments/', views.manage_course_assignments, name='manage_course_assignments'),

    path('assign-quiz-to-users/', views.assign_quiz_to_users, name='assign_quiz_to_users'),
    path('create-employee/', views.create_employee, name='create_employee'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups-list/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/add/', views.add_member_to_group, name='add_member_to_group'),
]