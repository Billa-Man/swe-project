from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from supabase import create_client, Client
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from core.models import LoginAttempt
from django.contrib import messages
from django.utils.timezone import now
import requests


from loguru import logger

def home(request):
    return render(request, 'core/home.html')

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
            logger.info("Database connection successful.")
            status['database'] = True
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        status['errors'].append(f"Database Error: {str(e)}")
    
    # Test Supabase Client Connection
    try:
        supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        # Try to fetch user (requires authentication)
        user = supabase.auth.get_user()
        logger.info("Supabase client connection successful.")
        status['supabase_client'] = True
    except Exception as e:
        status['errors'].append(f"Supabase Error: {str(e)}")
        logger.error(f"Supabase client connection error: {str(e)}")
    
    return JsonResponse(status)

def login_view(request):
    if request.method == 'POST':
        # Bind the form with POST data
        form = AuthenticationForm(request, data=request.POST)
        # Get common information
        ip_address = request.META.get('REMOTE_ADDR')
        browser_info = request.META.get('HTTP_USER_AGENT', 'Unknown')
        # Get the username from the POST data (this might be None if not provided)
        username = request.POST.get('username', None)
        
        # Validate the form
        if form.is_valid():
            user = form.get_user()
            success = True
        else:
            user = None
            success = False

        # Record the login attempt regardless of success
        LoginAttempt.objects.create(
            user=user,
            success=success,
            ip_address=ip_address,
            username=username,
            browser_info=browser_info,
        )

        # If successful, log the user in and redirect; otherwise, show an error
        if success:
            if user.is_superuser:
                messages.error(request, "Admins must login via /admin/")
                return render(request, 'account/login.html', {'form': form})
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'account/login.html', {'form': form})
    else:
        # Instantiate a blank authentication form
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})