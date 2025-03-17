from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def connection_check(request):
    data = {"message": "Connection check successful"}
    return JsonResponse(data, status=200)
