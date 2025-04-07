# --- forms.py ---
"""
this file contains forms setting for using crispy_form
"""
from django import forms
from django.contrib.auth.models import User
from .models import EmployeeGroup

class EmployeeCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    groups = forms.ModelMultipleChoiceField(
        queryset=EmployeeGroup.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

class GroupCreateForm(forms.ModelForm):
    employee_emails = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'user1@example.com, user2@example.com'}),
        required=False,
        help_text="Comma-separated list of emails"
    )

    class Meta:
        model = EmployeeGroup
        fields = ['name']
