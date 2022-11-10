from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.
class User(AbstractUser):
    profile = ProcessedImageField(
        blank=True,
        processors=[Thumbnail(120, 120)],
        format="JPEG",
        options={"quality": 90},
    )
    nickname = models.CharField(max_length=15, unique=True, null=True)
    
    def __str__(self):
        return self.email