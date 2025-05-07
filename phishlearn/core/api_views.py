from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .gophish_utils.campaigns import (
    get_campaigns,
    get_campaign_with_id,
    get_campaign_summary,
    create_campaign,
    delete_campaign,
    complete_campaign
)
from .gophish_utils.templates import get_templates
from .gophish_utils.landing_pages import get_landing_pages
from .gophish_utils.sending_profiles import get_sending_profiles
from .gophish_utils.users_and_groups import get_groups
import json

@login_required
def api_campaigns(request):
    """API endpoint to get all campaigns"""
    try:
        campaigns = get_campaigns()
        return JsonResponse(campaigns, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def api_campaign_detail(request, campaign_id):
    """API endpoint to get a specific campaign by ID"""
    try:
        campaign = get_campaign_with_id(campaign_id)
        return JsonResponse(campaign, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def api_campaign_summary(request, campaign_id):
    """API endpoint to get a campaign summary by ID"""
    try:
        summary = get_campaign_summary(campaign_id)
        return JsonResponse(summary, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def api_create_campaign(request):
    """API endpoint to create a new campaign"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'template', 'page', 'smtp', 'groups']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({"error": f"Missing required field: {field}"}, status=400)
        
        # Convert string IDs to integers
        try:
            template_id = int(data['template'])
            page_id = int(data['page'])
            smtp_id = int(data['smtp'])
            group_ids = [int(group_id) for group_id in data['groups']]
        except ValueError:
            return JsonResponse({"error": "Invalid ID format. All IDs must be numbers."}, status=400)
        
        # Create the campaign
        campaign = create_campaign(
            name=data['name'],
            template=template_id,
            page=page_id,
            smtp=smtp_id,
            groups=group_ids,
            launch_date=data.get('launch_date') or None
        )
        
        if campaign is None:
            return JsonResponse({"error": "Failed to create campaign"}, status=500)
        return JsonResponse(campaign, safe=False)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["DELETE"])
@csrf_exempt
def api_delete_campaign(request, campaign_id):
    """API endpoint to delete a campaign"""
    try:
        result = delete_campaign(campaign_id)
        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def api_complete_campaign(request, campaign_id):
    """API endpoint to mark a campaign as complete"""
    try:
        result = complete_campaign(campaign_id)
        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
def api_templates(request):
    """Get all email templates from GoPhish"""
    try:
        templates = get_templates()
        return JsonResponse(templates, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
def api_pages(request):
    """Get all landing pages from GoPhish"""
    try:
        pages = get_landing_pages()
        return JsonResponse(pages, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
def api_profiles(request):
    """Get all sending profiles from GoPhish"""
    try:
        profiles = get_sending_profiles()
        return JsonResponse(profiles, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
def api_groups(request):
    """Get all groups from GoPhish"""
    try:
        groups = get_groups()
        return JsonResponse(groups, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 