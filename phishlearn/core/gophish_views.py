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

from .gophish_utils.sending_profiles import (
    get_sending_profiles,
    get_sending_profile_with_id,
    create_sending_profile,
    modify_sending_profile,
    delete_sending_profile,
)

from .gophish_utils.landing_pages import (
    get_landing_pages,
    get_landing_page_with_id,
    create_landing_page,
    modify_landing_page,
    delete_landing_page,
)

@login_required
def control_center(request):
    """Display management interface for all GoPhish models"""
    templates = get_templates()
    pages = get_landing_pages()
    profiles = get_sending_profiles()
    
    context = {
        'templates': templates,
        'pages': pages,
        'profiles': profiles
    }
    
    return render(request, 'it_owner/control_center.html', context)

@login_required
def gophish_management(request):
    """Display users and groups for all GoPhish models"""
    users = get_users()
    groups = get_groups()

    context = {
        'users': users,
        'groups': groups,
    }

    return render(request, 'it_owner/gophish_management.html', context)

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
                role=role,
                password=password,
                username=username,
            )
            
            if not user:
                raise Exception("Failed to create user via API")
            return JsonResponse({"success": True, "message": "User created successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
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
            )
            
            if not result:
                return JsonResponse({"error": "Failed to update user"}, status=500)
            return JsonResponse({"success": True, "message": "User updated successfully"})            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        
    @method_decorator(login_required)
    def delete(self, request, user_id):
        """Delete a user"""
        try:
            result = delete_user(user_id)
            if not result:
                return JsonResponse({"error": f"Failed to delete user with ID {user_id}"}, status=500)
            return JsonResponse({"success": True, "message": "User deleted successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

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
                name=name,
                targets=targets,
            )
            
            if not group:
                raise Exception("Failed to create group via API")
            return JsonResponse({"success": True, "message": "Group created successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
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
            )
            
            if not result:
                return JsonResponse({"error": "Failed to update group"}, status=500)
            return JsonResponse({"success": True, "message": "Group updated successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        
    @method_decorator(login_required)
    def delete(self, request, group_id):
        """Delete a group"""
        try:
            result = delete_group(group_id)
            if not result:
                return JsonResponse({"error": f"Failed to delete group with ID {group_id}"}, status=500)
            return JsonResponse({"success": True, "message": "Group deleted successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

class CreateGroupFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'gophish/create_group.html')
    

##### GOPHISH TEMPLATES #####

@method_decorator(csrf_exempt, name='dispatch')
class TemplateView(View):
    
    @method_decorator(login_required)
    def get(self, request, template_id=None):

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
                name=name,
                subject=subject,
                text=text,
                html=html,
                attachments=attachments
            )
            
            if not template:
                raise Exception("Failed to create template via API")
            return JsonResponse({"success": True, "message": "Template created successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
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
                attachments=data.get("attachments", existing.get("attachments"))
            )
            
            if not result:
                return JsonResponse({"error": "Failed to update template"}, status=500)
            return JsonResponse({"success": True, "message": "Template updated successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        
    @method_decorator(login_required)
    def delete(self, request, template_id):
        try:
            result = delete_template(template_id)
            if not result:
                return JsonResponse({"error": f"Failed to delete template with ID {template_id}"}, status=500)
            return JsonResponse({"success": True, "message": "Template deleted successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

class CreateTemplateFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'gophish/create_template.html')
    

##### GOPHISH SENDING PROFILES #####

@method_decorator(csrf_exempt, name='dispatch')
class SendingProfileView(View):
    
    @method_decorator(login_required)
    def get(self, request, profile_id=None):
        """Handle GET requests for groups"""
        if profile_id:
            profile = get_sending_profile_with_id(profile_id)
            if not profile:
                return JsonResponse({"error": f"Sending Profile with ID {profile_id} not found"}, status=404)
            return JsonResponse(profile)
        else:
            profiles = get_sending_profiles()
            if profiles is None:
                return JsonResponse({"error": "Failed to retrieve sending profiles"}, status=500)
            
            data = [{"id": profile.get("id"), 
                    "name": profile.get("name"), 
                    "username": profile.get("username"),}
                   for profile in profiles]
            return JsonResponse({"profiles": data})
    
    @method_decorator(login_required)
    def post(self, request):
        """Create a new sending profile"""
        try:
            name = request.POST.get("name")
            username = request.POST.get("username")
            password = request.POST.get("password")
            host = request.POST.get("host")
            interface_type = request.POST.get("interface_type")
            from_address = request.POST.get("from_address")
            
            profile = create_sending_profile(
                name=name,
                username=username,
                password=password,
                host=host,
                interface_type=interface_type,
                from_address=from_address,
            )
            
            if not profile:
                raise Exception("Failed to create sending profile via API")
            return JsonResponse({"success": True, "message": "Sending Profile created successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
    @method_decorator(login_required)
    def put(self, request, profile_id):
        """Update an existing sending profile"""
        try:
            data = json.loads(request.body)
            
            existing = get_sending_profile_with_id(profile_id)
            if not existing:
                return JsonResponse({"error": f"Sending Profile with ID {profile_id} not found"}, status=404)
            
            result = modify_sending_profile(
                id=profile_id,
                name=data.get("name", existing.get("name")),
                username=data.get("username", existing.get("username")),
                password=data.get("password", existing.get("password")),
                host=data.get("host", existing.get("host")),
                from_address=data.get("from_address", existing.get("from_address")),
                interface_type=data.get("interface_type", existing.get("interface_type")),
                ignore_cert_errors=data.get("ignore_cert_errrors", existing.get("ignore_cert_errors")),
                profile_headers=data.get("headers", existing.get("headers")),
            )
            
            if not result:
                return JsonResponse({"error": "Failed to update sending profile"}, status=500)
            return JsonResponse({"success": True, "message": "Sending Profile updated successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        
    @method_decorator(login_required)
    def delete(self, request, profile_id):
        """Delete a sending profile"""
        try:
            result = delete_sending_profile(profile_id)
            if not result:
                return JsonResponse({"error": f"Failed to delete sending profile with ID {profile_id}"}, status=500)
            return JsonResponse({"success": True, "message": "Sending Profile deleted successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

class CreateSendingProfileFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'gophish/create_sending_profile.html')

##### GOPHISH LANDING PAGES #####

@method_decorator(csrf_exempt, name='dispatch')
class LandingPageView(View):
    
    @method_decorator(login_required)
    def get(self, request, page_id=None):
        """Handle GET requests for landing pages"""
        if page_id:
            page = get_landing_page_with_id(page_id)
            if not page:
                return JsonResponse({"error": f"Sending Profile with ID {page_id} not found"}, status=404)
            return JsonResponse(page)
        else:
            pages = get_landing_pages()
            if pages is None:
                return JsonResponse({"error": "Failed to retrieve landing pages"}, status=500)
            
            data = [{"id": page.get("id"), 
                    "name": page.get("name"), 
                    "redirect_url": page.get("redirect_url"),}
                   for page in pages]
            return JsonResponse({"pages": data})
    
    @method_decorator(login_required)
    def post(self, request):
        """Create a new landing page"""
        try:
            name = request.POST.get("name")
            html = request.POST.get("html")
            capture_credentials = request.POST.get("capture_credentials")
            capture_passwords = request.POST.get("capture_passwords")
            redirect_url = request.POST.get("redirect_url")
            
            profile = create_landing_page(
                name=name,
                html=html,
                capture_credentials=capture_credentials,
                capture_passwords=capture_passwords,
                redirect_url=redirect_url,
            )
            
            if not profile:
                raise Exception("Failed to create landing page via API")
            return JsonResponse({"success": True, "message": "Landing Page created successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
    @method_decorator(login_required)
    def put(self, request, page_id):
        """Update an existing landing page"""
        try:
            data = json.loads(request.body)
            existing = get_landing_page_with_id(page_id)

            if not existing:
                return JsonResponse({"error": f"Landing Page with ID {page_id} not found"}, status=404)
            
            result = modify_landing_page(
                id=page_id,
                name=data.get("name", existing.get("name")),
                html=data.get("html", existing.get("html")),
                capture_credentials=data.get("capture_credentials", existing.get("capture_credentials")),
                capture_passwords=data.get("capture_passwords", existing.get("capture_passwords")),
                redirect_url=data.get("redirect_url", existing.get("redirect_url")),
            )
            
            if not result:
                return JsonResponse({"error": "Failed to update landing page"}, status=500)
            return JsonResponse({"success": True, "message": "Landing page updated successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        
    @method_decorator(login_required)
    def delete(self, request, page_id):
        """Delete a Landing Page"""
        try:
            result = delete_landing_page(page_id)
            if not result:
                return JsonResponse({"error": f"Failed to delete landing page with ID {page_id}"}, status=500)
            return JsonResponse({"success": True, "message": "Landing Page deleted successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

class CreateLandingPageFormView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'gophish/create_landing_page.html')