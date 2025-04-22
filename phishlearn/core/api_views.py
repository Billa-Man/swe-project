from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .gophish_utils.campaigns import (
    get_campaigns,
    get_campaign_with_id,
    get_campaign_summary
)

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