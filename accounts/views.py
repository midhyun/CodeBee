from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

# Create your views here.
# test용도
def index(request):
    persons = get_user_model().objects.order_by("-pk")
    return render(request, "accounts/index.html", {"persons": persons,})

def detail(request, user_pk):
    person = get_object_or_404(get_user_model(), pk=user_pk)
    return render(request, "accounts/detail.html", {"person" : person,})