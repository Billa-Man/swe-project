from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
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
    CourseProgress,
    CourseAssignment
)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fields = ('user_type', 'organization', 'created_at')
    readonly_fields = ('created_at',)

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'get_full_name', 'get_user_type', 'get_organization', 'get_status', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'userprofile__user_type', 'userprofile__organization', 'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'userprofile__organization')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name or obj.last_name else obj.username
    get_full_name.short_description = 'Full Name'
    
    def get_user_type(self, obj):
        try:
            return obj.userprofile.get_user_type_display()
        except UserProfile.DoesNotExist:
            return 'N/A'
    get_user_type.short_description = 'User Type'
    
    def get_organization(self, obj):
        try:
            return obj.userprofile.organization or 'N/A'
        except UserProfile.DoesNotExist:
            return 'N/A'
    get_organization.short_description = 'Organization'

    def get_status(self, obj):
        status = []
        if obj.is_active:
            if obj.is_superuser:
                return format_html('<span style="color: #dc3545;">Superuser</span>')
            elif obj.is_staff:
                return format_html('<span style="color: #28a745;">Staff</span>')
            else:
                return format_html('<span style="color: #007bff;">Active</span>')
        return format_html('<span style="color: #6c757d;">Inactive</span>')
    get_status.short_description = 'Status'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'organization', 'created_at')
    list_filter = ('user_type', 'organization', 'created_at')
    search_fields = ('user__username', 'user__email', 'organization')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_at', 'is_published')
    list_filter = ('created_at', 'updated_at', 'is_published')
    search_fields = ('title', 'description')
    list_editable = ('is_published',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'description')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('question_text',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('choice_text',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed_at')
    list_filter = ('completed_at', 'score')
    search_fields = ('user__email',)

@admin.register(PhishingTemplate)
class PhishingTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'subject', 'content')

@admin.register(PhishingTest)
class PhishingTestAdmin(admin.ModelAdmin):
    list_display = ('template', 'sent_by', 'sent_to', 'sent_at', 'clicked', 'clicked_at')
    list_filter = ('sent_at', 'clicked')
    search_fields = ('sent_to__email', 'sent_by__email')

@admin.register(EmployeeGroup)
class EmployeeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'it_owner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'it_owner__email')
    filter_horizontal = ('employees',)

@admin.register(CourseCompletion)
class CourseCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'score', 'completed_at')
    list_filter = ('completed_at', 'score')
    search_fields = ('user__email', 'course__title')

@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'started_at')
    list_filter = ('started_at',)
    search_fields = ('user__email', 'course__title')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'message')

@admin.register(CourseAssignment)
class CourseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'assigned_by', 'assigned_date', 'due_date')
    list_filter = ('assigned_date', 'due_date')
    search_fields = ('user__email', 'course__title', 'assigned_by__email')