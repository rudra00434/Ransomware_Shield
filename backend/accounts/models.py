from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Using email as username
    email = models.EmailField(unique=True)
    
    SUBSCRIPTION_CHOICES = [
        ('FREE', 'Free'),
        ('PRO', 'Pro'),
        ('ENTERPRISE', 'Enterprise'),
    ]
    subscription_tier = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='FREE')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
