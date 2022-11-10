from . import views
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    ### 소셜로그인 ###
    path("login/kakao/", views.kakao_request, name="kakao"),
    path("login/kakao/callback/", views.kakao_callback),
    path("login/naver/", views.naver_request, name="naver"),
    path("login/naver/callback/", views.naver_callback),
    path("login/google/", views.google_request, name="google"),
    path("login/google/callback/", views.google_callback),
    path("login/github/", views.github_request, name="github"),
    path("login/github/callback/", views.github_callback),
    ### 소셜로그인 ###
]
