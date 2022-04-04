from django import forms 
from django.core.exceptions import ValidationError
from .models import Issue

class IssueForm(forms.ModelForm):
    
    class Meta:
        model = Issue
        fields = ('user', 'email', 'subject', 'discription',)