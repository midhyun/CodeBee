from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField()


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models)
    title = models.CharField(max_length=80)
    content = models.TextField()
    category = models.CharField(max_length=80)
    image = ProcessedImageField(
        upload_to='articles',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={
            'quality': 90,
        }

    )
    study_type = models.CharField(max_length=80)
    location = models.CharField(max_length=100)
    tags = models.CharField(max_length=50)
    x = models.IntegerField(default= 0)
    y = models.IntegerField(default= 0)
    limit = models.IntegerField(default=1)
    deadline = models.DateField(auto_now_add=True,blank=True)
