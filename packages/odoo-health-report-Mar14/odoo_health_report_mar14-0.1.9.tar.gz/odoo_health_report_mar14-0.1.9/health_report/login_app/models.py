from django.db import models

# Create your models here.

from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class OdooSetup(models.Model):
    url = models.CharField(max_length=255)
    database_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # Avoid double hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.database_name} - {self.url}"
