from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
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
    TrainingModule,
    Notification
)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    list_filter = ('is_staff', 'is_superuser', 'userprofile__user_type')
    
    def get_user_type(self, obj):
        try:
            return obj.userprofile.user_type
        except UserProfile.DoesNotExist:
            return 'N/A'
    get_user_type.short_description = 'User Type'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'organization', 'created_at')
    list_filter = ('user_type', 'organization')
    search_fields = ('user__email', 'organization')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'description')
    list_filter = ('course',)
    search_fields = ('title', 'description')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed_at')
    list_filter = ('completed_at', 'quiz')
    search_fields = ('user__email',)

@admin.register(PhishingTemplate)
class PhishingTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'subject', 'content')

@admin.register(PhishingTest)
class PhishingTestAdmin(admin.ModelAdmin):
    list_display = ('template', 'sent_by', 'sent_to', 'sent_at', 'clicked', 'clicked_at')
    list_filter = ('clicked', 'sent_at')
    search_fields = ('template__title', 'sent_by__email', 'sent_to__email')

@admin.register(EmployeeGroup)
class EmployeeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'it_owner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'it_owner__email')
    filter_horizontal = ('employees',)

@admin.register(TrainingModule)
class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    list_filter = ('title',)
    search_fields = ('title', 'description')

# @admin.register(ModuleCompletion)
# class ModuleCompletionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'module', 'score', 'completed_at')
#     list_filter = ('completed_at', 'score')
#     search_fields = ('user__email',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at', 'link')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'message')