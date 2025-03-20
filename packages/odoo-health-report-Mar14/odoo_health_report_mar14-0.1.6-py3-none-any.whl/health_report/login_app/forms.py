import xmlrpc.client
from django import forms
from django.core.exceptions import ValidationError
from .models import OdooSetup

class OdooSetupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password'}))

    class Meta:
        model = OdooSetup
        fields = ['url', 'database_name', 'username', 'password']

    def clean(self):
        data = self.cleaned_data
        url = data.get('url')
        database_name = data.get('database_name')
        username = data.get('username')
        password = data.get('password')
        if url and database_name and username and password:
            try:
                # Connect to Odoo authentication API
                common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
                uid = common.authenticate(database_name, username, password, {})

                # If authentication fails, Odoo returns False
                if not uid:
                    raise ValidationError("Could not authenticate with Odoo. Check credentials.")
            except Exception as e:
                raise ValidationError(f"Connection error: {str(e)}")

        return super().clean()
