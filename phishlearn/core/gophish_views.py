from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .gophish_utils.templates import (
    get_templates, 
    get_template_with_id, 
    create_template, 
    modify_template, 
    delete_template
)

from .gophish_utils.user_management import (
    get_users,
    get_user_with_id,
    create_user,
    modify_user,
    delete_user,
)

from .gophish_utils.users_and_groups import (
    get_groups,
    get_group_with_id,
    create_group,
    modify_group,
    delete_group,
)


@login_required
def gophish_management(request):
    """Display management interface for all GoPhish models"""
    templates = get_templates()
    users = get_users()
    groups = get_groups()
    
    context = {
        'templates': templates,
        'users': users,
        'groups': groups
    }
    
    return render(request, 'it_owner/gophish_management.html', context)

##### GOPHISH TEMPLATES #####

@method_decorator(csrf_exempt, name='dispatch')
class TemplateView(View):
    
    @method_decorator(login_required)
    def get(self, request, template_id=None):
        """Handle GET requests for templates"""
        if template_id:
            template = get_template_with_id(template_id)
            if not template:
                return JsonResponse({"error": f"Template with ID {template_id} not found"}, status=404)
            return JsonResponse(template)
        else:
            templates = get_templates()
            if templates is None:
                return JsonResponse({"error": "Failed to retrieve templates"}, status=500)
            
            data = [{"id": template.get("id"), 
                    "name": template.get("name"), 
                    "subject": template.get("subject"),}
                   for template in templates]
            return JsonResponse({"templates": data})
    
    @method_decorator(login_required)
    def post(self, request):
        """Create a new template"""
        try:
            name = request.POST.get("name")
            subject = request.POST.get("subject")
            text = request.POST.get("text")
            html = request.POST.get("html")
            attachments = json.loads(request.POST.get("attachments", "{}"))
            
            template = create_template(
                id=None,
                name=name,
                subject=subject,
                text=text,
                html=html,
                modified_date=None,
                attachments=attachments
            )
            
            if not template:
                raise Exception("Failed to create template via API")
                
            return redirect('template_detail', template_id=template.get("id"))
        except Exception as e:
            return render(request, 'gophish/create_template.html', {
                'error': str(e)
            })
    
    @method_decorator(login_required)
    def put(self, request, template_id):
        """Update an existing template"""
        try:
            data = json.loads(request.body)
            
            existing = get_template_with_id(template_id)
            if not existing:
                return JsonResponse({"error": f"Template with ID {template_id} not found"}, status=404)
            
            result = modify_template(
                id=template_id,
                name=data.get("name", existing.get("name")),
                subject=data.get("subject", existing.get("subject")),
                text=data.get("text", existing.get("text")),
                html=data.get("html", existing.get("html")),
                modified_date=None,
                attachments=data.get("attachments", existing.get("attachments"))
            )
            
            if not result:
                return JsonResponse({"error": "Failed to update template"}, status=500)
                
            return JsonResponse({"message": "Template updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    @method_decorator(login_required)
    def delete(self, request, template_id):
        """Delete a template"""
        try:
            result = delete_template(template_id)
            if not result:
                return JsonResponse({"error": f"Failed to delete template with ID {template_id}"}, status=500)
                
            return JsonResponse({"message": "Template deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class CreateTemplateFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'gophish/create_template.html')
    
##### GOPHISH USERS #####

@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    
    @method_decorator(login_required)
    def get(self, request, user_id=None):
        """Handle GET requests for users"""
        if user_id:
            user = get_user_with_id(user_id)
            if not user:
                return JsonResponse({"error": f"User with ID {user_id} not found"}, status=404)
            return JsonResponse(user)
        else:
            users = get_users()
            if users is None:
                return JsonResponse({"error": "Failed to retrieve users"}, status=500)
            
            data = [{"id": user.get("id"), 
                    "role": user.get("role"), 
                    "username": user.get("username"),}
                   for user in users]
            return JsonResponse({"users": data})
    
    @method_decorator(login_required)
    def post(self, request):
        """Create a new user"""
        try:
            role = json.loads(request.POST.get("role"))
            password = request.POST.get("password")
            username = request.POST.get("username")
            
            user = create_user(
                id=None,
                role=role,
                password=password,
                username=username,
                modified_date=None,
            )
            
            if not user:
                raise Exception("Failed to create user via API")
                
            return redirect('user_detail', user_id=user.get("id"))
        except Exception as e:
            return render(request, 'gophish/create_user.html', {
                'error': str(e)
            })
    
    @method_decorator(login_required)
    def put(self, request, user_id):
        """Update an existing user"""
        try:
            data = json.loads(request.body)
            
            existing = get_user_with_id(user_id)
            if not existing:
                return JsonResponse({"error": f"User with ID {user_id} not found"}, status=404)
            
            result = modify_user(
                id=user_id,
                role=data.get("role", existing.get("role")),
                password=data.get("password", existing.get("password")),
                username=data.get("username", existing.get("username")),
                modified_date=None
            )
            
            if not result:
                return JsonResponse({"error": "Failed to update user"}, status=500)
            return JsonResponse({"message": "User updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    @method_decorator(login_required)
    def delete(self, request, user_id):
        """Delete a user"""
        try:
            result = delete_user(user_id)
            if not result:
                return JsonResponse({"error": f"Failed to delete user with ID {user_id}"}, status=500)
            return JsonResponse({"message": "User deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class CreateUserFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'gophish/create_user.html')
    
##### GOPHISH GROUPS #####

@method_decorator(csrf_exempt, name='dispatch')
class GroupView(View):
    
    @method_decorator(login_required)
    def get(self, request, group_id=None):
        """Handle GET requests for groups"""
        if group_id:
            group = get_group_with_id(group_id)
            if not group:
                return JsonResponse({"error": f"Group with ID {group_id} not found"}, status=404)
            return JsonResponse(group)
        else:
            groups = get_groups()
            if groups is None:
                return JsonResponse({"error": "Failed to retrieve groups"}, status=500)
            
            data = [{"id": group.get("id"), 
                    "name": group.get("name"), 
                    "targets": group.get("targets"),}
                   for group in groups]
            return JsonResponse({"groups": data})
    
    @method_decorator(login_required)
    def post(self, request):
        """Create a new group"""
        try:
            targets = json.loads(request.POST.get("targets"))
            name = request.POST.get("name")
            
            group = create_group(
                id=None,
                name=name,
                targets=targets,
                modified_date=None,
            )
            
            if not group:
                raise Exception("Failed to create group via API")
                
            return redirect('group_detail', group_id=group.get("id"))
        except Exception as e:
            return render(request, 'gophish/create_group.html', {
                'error': str(e)
            })
    
    @method_decorator(login_required)
    def put(self, request, group_id):
        """Update an existing group"""
        try:
            data = json.loads(request.body)
            
            existing = get_group_with_id(group_id)
            if not existing:
                return JsonResponse({"error": f"Group with ID {group_id} not found"}, status=404)
            
            result = modify_group(
                id=group_id,
                name=data.get("name", existing.get("name")),
                targets=data.get("targets", existing.get("targets")),
                modified_date=None
            )
            
            if not result:
                return JsonResponse({"error": "Failed to update group"}, status=500)
            return JsonResponse({"message": "Group updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    @method_decorator(login_required)
    def delete(self, request, group_id):
        """Delete a group"""
        try:
            result = delete_group(group_id)
            if not result:
                return JsonResponse({"error": f"Failed to delete group with ID {group_id}"}, status=500)
            return JsonResponse({"message": "Group deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class CreateGroupFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'gophish/create_group.html')