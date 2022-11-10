from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
def detail(request, user_pk):
    person = get_user_model().objects.get(pk=user_pk)
    return render(request, "accounts/detail.html", {"person" : person,})