from django.urls import path
from . import views

app_name = 'gcalendar'

urlpatterns = [
    path('', views.test, name='test'),
    path('google_call', views.google_call, name='google_call'),
    path('google_code', views.google_code, name='google_code'),
]