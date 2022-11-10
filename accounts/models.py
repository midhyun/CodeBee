from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=15, unique=True, null=True)
    
    def __str__(self):
        return self.email