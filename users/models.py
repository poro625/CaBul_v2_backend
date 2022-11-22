from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings

# Create your models here.
class User(AbstractUser): 
    email = models.EmailField(verbose_name = "email", max_length = 255, unique = True)
    username = models.CharField(max_length=30)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']
    