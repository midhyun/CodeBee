from django.contrib import admin
from .models import Study, Comment
from .forms import CommentForm

# Register your models here.
admin.site.register([Study])

@admin.register(Comment)
class CountryAmin(admin.ModelAdmin):
    form = CommentForm