from django.urls import path
from . import views
from .views import LandingPagesView
from .api_views import api_campaigns, api_campaign_detail, api_campaign_summary

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('manage-employees/', views.list_employees, name='manage_employees'),
    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('manage-templates/', views.manage_templates, name='manage_templates'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('assign-quiz-to-users/', views.assign_quiz_to_users, name='assign_quiz_to_users'),
    path('create-employee/', views.create_employee, name='create_employee'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups-list/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/add/', views.add_member_to_group, name='add_member_to_group'),
    path('employees/<int:employee_id>/delete/', views.delete_emplpoyee, name='delete_employee'),
    path('groups/<int:group_id>/remove/<int:employee_id>/', views.remove_employee_from_group, name='remove_employee_from_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<int:course_id>/', views.course_view, name='course_view'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('change-password/', views.change_password, name='change_password'),


    path('sending-profiles/', views.SendingProfilesView.as_view(), name='sending_profiles'),
    path('sending-profiles/modify/', views.ModifySendingProfileView.as_view(), name='modify_sending_profile'),
    path('sending-profiles/delete/', views.DeleteSendingProfileView.as_view(), name='delete_sending_profile'),


    path('landing_pages/', views.LandingPagesView.as_view(), name='landing_pages'),
    path('gophish-analytics/', views.gophish_analytics, name='gophish_analytics'),
    
    # API endpoints for Gophish campaigns
    path('api/gophish/campaigns/', api_campaigns, name='api_campaigns'),
    path('api/gophish/campaigns/<int:campaign_id>/', api_campaign_detail, name='api_campaign_detail'),
    path('api/gophish/campaigns/<int:campaign_id>/summary/', api_campaign_summary, name='api_campaign_summary'),
    path("reset-api-key/", views.reset_api_key_view, name="reset_api_key"),  

    path('templates/', views.get_templates, name='get_templates'),
    path('templates/<int:template_id>/', views.get_template_by_id, name='get_template_by_id'),
    path('templates/create/', views.create_template, name='create_template'),
    path('templates/<int:template_id>/update/', views.modify_template, name='modify_template'),
    path('templates/<int:template_id>/delete/', views.delete_template, name='delete_template'),
    
    # User URLs
    path('users/', views.get_users, name='get_users'),
    path('users/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/update/', views.modify_user, name='modify_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # Group URLs
    path('groups/', views.get_groups, name='get_groups'),
    path('groups/<int:group_id>/', views.get_group_by_id, name='get_group_by_id'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/update/', views.modify_group, name='modify_group'),
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),

    path('gophish/management/', views.gophish_management, name='gophish_management'),

]