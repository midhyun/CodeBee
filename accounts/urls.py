from django.urls import path, re_path
from . import views


app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:user_pk>/", views.detail, name="detail"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    re_path(
        r"^login/(?P<service_name>[^/]+)/$", views.social_login_request, name="social"
    ),
    re_path(r"^login/(?P<service_name>[^/]+)/callback/$", views.social_login_callback),
    path("test/", views.test, name="test"),
    path('likes/<int:user_pk>/', views.likes, name='likes'),
    path('dislikes/<int:user_pk>/', views.dislikes, name='dislikes'),
]
