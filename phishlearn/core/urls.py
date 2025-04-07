from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('send-phishing-test/', views.send_phishing_test, name='send_phishing_test'),
    path('manage-employees/', views.manage_employees, name='manage_employees'),
    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('manage-templates/', views.manage_templates, name='manage_templates'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('assign-quiz-to-users/', views.assign_quiz_to_users, name='assign_quiz_to_users'),
] 