from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_operation = models.BooleanField(default=False)
    # is_supplier = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_ppc = models.BooleanField(default=False)