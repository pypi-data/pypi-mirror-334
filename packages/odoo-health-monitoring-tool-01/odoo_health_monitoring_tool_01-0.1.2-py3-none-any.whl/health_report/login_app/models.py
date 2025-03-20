from django.db import models

# Create your models here.

from django.contrib.auth.hashers import make_password, check_password
from django.db import models
import xmlrpc
from django.core.exceptions import ValidationError

class OdooSetup(models.Model):
    url = models.CharField(max_length=255)
    database_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    api_token = models.CharField(max_length=255)

    def clean(self):
        if not self.api_token:
            raise ValidationError({
                'api_token':"Please provide a valid api token."
            })
        url = self.url
        database_name = self.database_name
        username = self.username
        password = self.api_token
        
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

    def __str__(self):
        return f"{self.database_name} - {self.url}"
