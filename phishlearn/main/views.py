from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from supabase import create_client, Client
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def connection_check(request):
    status = {
        'database': False,
        'supabase_client': False,
        'errors': [],
        'debug': {
            'supabase_url': settings.SUPABASE_URL,
            'supabase_key': bool(settings.SUPABASE_KEY)  # Only show if key exists, not the actual key
        }
    }
    
    # Test Database Connection
    try:
        with connections['default'].cursor() as cursor:
            cursor.execute('SELECT 1')
            status['database'] = True
    except Exception as e:
        status['errors'].append(f"Database Error: {str(e)}")
    
    # Test Supabase Client Connection
    try:
        supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        # Try to fetch user (requires authentication)
        user = supabase.auth.get_user()
        status['supabase_client'] = True
    except Exception as e:
        status['errors'].append(f"Supabase Error: {str(e)}")
    
    return JsonResponse(status)

