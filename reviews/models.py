from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class Study(models.Model):
    limits = models.IntegerField(default=4)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=30)
    content = models.TextField()
    tag = models.CharField(max_length=20, blank=True)
    categorie = models.CharField(max_length=30)
    study_type = models.CharField(max_length=30)
    deadline = models.DateField()
    location_type = models.BooleanField(default=False)  # False - 오프라인
    location = models.CharField(max_length=50, blank=True)
    X = models.CharField(max_length=20, null=True)
    Y = models.CharField(max_length=20, null=True)
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        format="JPEG",
    )
    joined_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="joined")


class Accepted(models.Model):
    joined = models.BooleanField(default=False)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField()
