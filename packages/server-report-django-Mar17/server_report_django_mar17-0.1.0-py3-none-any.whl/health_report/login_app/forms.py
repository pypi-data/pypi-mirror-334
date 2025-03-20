import xmlrpc.client
from django import forms
from django.core.exceptions import ValidationError
from .models import OdooSetup

class OdooSetupForm(forms.ModelForm):
    api_token = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'api_token'}))

    class Meta:
        model = OdooSetup
        fields = ['url', 'database_name', 'username', 'api_token']

