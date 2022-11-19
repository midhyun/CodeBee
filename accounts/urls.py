from django.urls import path, re_path
from . import views


app_name = "accounts"

urlpatterns = [
    path("test/", views.test, name="test"),  # 테스트 페이지
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("<int:user_pk>/", views.detail, name="detail"),
    path("<int:user_pk>/update/", views.update, name="update"),
    re_path(
        r"^login/(?P<service_name>[^/]+)/$", views.social_signup_request, name="social"
    ),
    re_path(r"^login/(?P<service_name>[^/]+)/callback/$", views.social_signup_callback),
    path("sns-logout/<str:service_name>/", views.sns_logout, name="sns-logout"),
    path("<int:user_pk>/likes/", views.likes, name="likes"),
    path("<int:user_pk>/dislikes/", views.dislikes, name="dislikes"),
    path("<int:user_pk>/password/", views.password_change, name="password-change"),
    path("<int:user_pk>/update/check/", views.check, name="check"),
    path("<int:user_pk>/update/phone-auth/", views.phone_auth, name="phone-auth"),
    path("<int:user_pk>/update/check-auth/", views.check_auth, name="check-auth"),
    path("<int:user_pk>/update/send-email/", views.send_email, name="send-email"),
    re_path(
        r"^([a-zA-Z0-9][^/]+)/update/send-email/([a-zA-Z0-9][^/]+)/([a-zA-Z0-9][^/]+)/email-auth/$",
        views.check_email_auth,
        name="check-email-auth",
    ),
    path('test2/',views.test2, name='test2')
]
