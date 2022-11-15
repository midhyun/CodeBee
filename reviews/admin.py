from django.contrib import admin
from .models import Study, Comment

# Register your models here.
admin.site.register([Study, Comment])