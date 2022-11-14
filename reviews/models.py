from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Study(models.Model):
    limits = models.IntegerField(default=4, validators=[MinValueValidator(2)])
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=30)
    content = models.TextField()
    tag = models.CharField(max_length=50, blank=True)
    categorie = models.CharField(max_length=30)
    study_type = models.CharField(max_length=30)
    deadline = models.DateTimeField(blank=True)
    location_type = models.BooleanField(default=False) # False 오프라인, True 온라인
    location = models.CharField(max_length=50, blank=True)
    X = models.CharField(max_length=20, null=True)
    Y = models.CharField(max_length=20, null=True)
    image = models.ImageField(
        upload_to="images/",
        blank=True,
    )
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 80},
    )


class Accepted(models.Model):
    joined = models.BooleanField(default=False) # False 신청상태, True 승인상태
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    joindate = models.DateTimeField(auto_now=True)


class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
