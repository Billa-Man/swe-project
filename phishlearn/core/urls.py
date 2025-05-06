from django.urls import path
from . import views, gophish_views
from .views import LandingPagesView
from .api_views import (
    api_campaigns,
    api_campaign_detail,
    api_campaign_summary,
    api_create_campaign,
    api_delete_campaign,
    api_complete_campaign,
    api_templates,
    api_pages,
    api_profiles,
    api_groups
)

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
    path('employees/<int:employee_id>/delete/', views.delete_employee, name='delete_employee'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<int:course_id>/', views.course_view, name='course_view'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('change-password/', views.change_password, name='change_password'),

    path('landing_pages/', views.LandingPagesView.as_view(), name='landing_pages'),
    path('gophish-analytics/', views.gophish_analytics, name='gophish_analytics'),
    
    # API endpoints for Gophish campaigns
    path('api/gophish/campaigns/', api_campaigns, name='api_campaigns'),
    path('api/gophish/campaigns/<int:campaign_id>/', api_campaign_detail, name='api_campaign_detail'),
    path('api/gophish/campaigns/<int:campaign_id>/summary/', api_campaign_summary, name='api_campaign_summary'),
    path('api/gophish/campaigns/create/', api_create_campaign, name='api_create_campaign'),
    path('api/gophish/campaigns/<int:campaign_id>/delete/', api_delete_campaign, name='api_delete_campaign'),
    path('api/gophish/campaigns/<int:campaign_id>/complete/', api_complete_campaign, name='api_complete_campaign'),
    path('api/gophish/templates/', api_templates, name='api_templates'),
    path('api/gophish/pages/', api_pages, name='api_pages'),
    path('api/gophish/profiles/', api_profiles, name='api_profiles'),
    path('api/gophish/groups/', api_groups, name='api_groups'),
    path("reset-api-key/", views.reset_api_key_view, name="reset_api_key"),  

    # Group URLs
    path('groups/', gophish_views.GroupView.as_view(), name='group_list'),
    path('groups/<int:group_id>/', gophish_views.GroupView.as_view(), name='group_detail'),
    path('groups/create/', gophish_views.CreateGroupFormView.as_view(), name='create_group_form'),

    # User URLs
    path('users/', gophish_views.UserView.as_view(), name='user_list'),
    path('users/<int:user_id>/', gophish_views.UserView.as_view(), name='user_detail'),
    path('users/create/', gophish_views.CreateUserFormView.as_view(), name='create_user_form'),

    # Template URLs
    path('templates/', gophish_views.TemplateView.as_view(), name='template_list'),
    path('templates/<int:template_id>/', gophish_views.TemplateView.as_view(), name='template_detail'),
    path('templates/create/', gophish_views.CreateTemplateFormView.as_view(), name='create_template_form'),

    # Sending Profile URLs
    path('profiles/', gophish_views.SendingProfileView.as_view(), name='profile_list'),
    path('profiles/<int:profile_id>/', gophish_views.SendingProfileView.as_view(), name='profile_detail'),
    path('profiles/create/', gophish_views.CreateSendingProfileFormView.as_view(), name='create_profile_form'),

    # Landing Page URLs
    path('pages/', gophish_views.LandingPageView.as_view(), name='page_list'),
    path('pages/<int:page_id>/', gophish_views.LandingPageView.as_view(), name='page_detail'),
    path('pages/create/', gophish_views.CreateLandingPageFormView.as_view(), name='create_page_form'),

    # Campaign URLs
    path('campaigns/', views.gophish_campaigns, name='gophish_campaigns'),
    path('gophish/control_center/', gophish_views.control_center, name='control_center'),
    path('gophish/management/', gophish_views.gophish_management, name='gophish_management'),

]