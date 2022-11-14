import secrets
import requests
from django.views import View
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from reviews.models import Study

# 소셜 로그인에 필요한 토큰 생성
state_token = secrets.token_urlsafe(16)

# 테스트용 html 페이지
def test(request):
    context = {
        "uid": request.user,
    }
    return render(request, "accounts/test.html", context)


# Create your views here.
def signup(request):
    if request.method == "POST":
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            # 주소
            user.location = request.POST["addr1"] + " " + request.POST["addr2"]
            # 휴대폰 번호
            user.phone = (
                request.POST["phone"][:3]
                + "-"
                + request.POST["phone"][3:7]
                + "-"
                + request.POST["phone"][7:]
            )
            user.save()
            user_login(request, user)
            return redirect("accounts:login")
    else:
        signup_form = CustomUserCreationForm()
    context = {
        "signup_form": signup_form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user_login(request, login_form.get_user())
            return redirect(request.GET.get("next") or "reviews:index")
    else:
        login_form = AuthenticationForm()
    context = {
        "login_form": login_form,
    }
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    user_logout(request)
    return redirect("accounts:login")


@login_required
def update(request, pk):
    user_logout(request)
    return redirect("accounts:login")


def social_login_request(request, service_name):
    google_base_url = "https://www.googleapis.com/auth"
    google_email = "/userinfo.email"
    google_myinfo = "/userinfo.profile"
    services = {
        "kakao": {
            "base_url": "https://kauth.kakao.com/oauth/authorize",
            "client_id": "9d90b5b2d651fe7e6adf2c2e261aaad3",
            "redirect_uri": "http://localhost:8000/accounts/login/kakao/callback",
            "response_type": "code",
        },
        "naver": {
            "base_url": "https://nid.naver.com/oauth2.0/authorize",
            "client_id": "I9ScPHTpJ9smDz9KyjoX",  # 배포시 보안적용 해야함
            "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
            "response_type": "code",
            "state": secrets.token_urlsafe(16),
        },
        "google": {
            "base_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "client_id": "925373116590-t4uf2ra8bkt25vegkjoskvi6054hd27u.apps.googleusercontent.com",  # 배포시 보안적용 해야함
            "redirect_uri": "http://localhost:8000/accounts/login/google/callback",
            "response_type": "code",
            "scope": f"{google_base_url}{google_email}+{google_base_url}{google_myinfo}",
        },
        "github": {
            "base_url": "https://github.com/login/oauth/authorize",
            "client_id": "481bbe1d16187fdb9f0e",  # 배포시 보안적용 해야함
            "redirect_uri": "http://localhost:8000/accounts/login/github/callback",
            "scope": "read:user",
        },
    }
    for k, v in services[service_name].items():
        if k == "base_url":
            res = f"{v}?"
        else:
            res += f"{k}={v}&"
    return redirect(res)


def social_login_callback(request, service_name):
    services = {
        "kakao": {
            "data": {
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:8000/accounts/login/kakao/callback",
                "client_id": "9d90b5b2d651fe7e6adf2c2e261aaad3",  # 배포시 보안적용 해야함
                "code": request.GET.get("code"),
            },
            "api": "https://kauth.kakao.com/oauth/token",
            "user_api": "https://kapi.kakao.com/v2/user/me",
        },
        "naver": {
            "data": {
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
                "client_id": "I9ScPHTpJ9smDz9KyjoX",  # 배포시 보안적용 해야함
                "client_secret": "4QJHVHKrOp",  # 배포시 보안적용 해야함
                "state": request.GET.get("state"),
                "code": request.GET.get("code"),
            },
            "api": "https://nid.naver.com/oauth2.0/token",
            "user_api": "https://openapi.naver.com/v1/nid/me",
        },
        "google": {
            "data": {
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:8000/accounts/login/google/callback",
                "client_id": "925373116590-t4uf2ra8bkt25vegkjoskvi6054hd27u.apps.googleusercontent.com",  # 배포시 보안적용 해야함
                "client_secret": "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",  # 배포시 보안적용 해야함
                "state": request.GET.get("state"),
                "code": request.GET.get("code"),
            },
            "api": "https://oauth2.googleapis.com/token",
            "user_api": "https://www.googleapis.com/oauth2/v3/userinfo",
        },
        "github": {
            "data": {
                "redirect_uri": "http://localhost:8000/accounts/login/github/callback",
                "client_id": "481bbe1d16187fdb9f0e",  # 배포시 보안적용 해야함
                "client_secret": "aaf7c5464bab25ff7a703f02a51b68803031fde3",  # 배포시 보안적용 해야함
                "code": request.GET.get("code"),
            },
            "api": "https://github.com/login/oauth/access_token",
            "user_api": "https://api.github.com/user",
        },
    }
    if service_name == "github":
        headers = {
            "accept": "application/json",
        }
        access_token = requests.post(
            services[service_name]["api"],
            data=services[service_name]["data"],
            headers=headers,
        ).json()["access_token"]
    else:
        access_token = requests.post(
            services[service_name]["api"], data=services[service_name]["data"]
        ).json()["access_token"]

    payload = {
        "kakao": {"Authorization": f"bearer ${access_token}"},
        "naver": {"Authorization": f"bearer {access_token}"},
        "google": {"access_token": f"{access_token}"},
        "github": {"Authorization": f"token {access_token}"},
    }

    if service_name == "google":
        params = payload[service_name]
        u_info = requests.get(services[service_name]["user_api"], params=params).json()
    else:
        headers = payload[service_name]
        u_info = requests.get(
            services[service_name]["user_api"], headers=headers
        ).json()
    print(u_info)
    print(access_token)
    if service_name == "kakao":
        login_data = {
            "kakao": {
                "social_id": u_info["id"],
                "username": u_info["properties"]["nickname"],
                "social_profile_picture": u_info["properties"]["profile_image"],
                "nickname": u_info["properties"]["nickname"],
                # "email": u_info["kakao_account"]["email"],
                "phone": None,
            },
        }
    elif service_name == "naver":
        login_data = {
            "naver": {
                "social_id": u_info["response"]["id"],
                "username": u_info["response"]["nickname"],
                "social_profile_picture": u_info["response"]["profile_image"],
                "nickname": u_info["response"]["name"],
                "email": u_info["response"]["email"],
                "phone": u_info["response"]["mobile"],
            },
        }
    elif service_name == "google":
        login_data = {
            "google": {
                "social_id": u_info["sub"],
                "username": u_info["name"],
                "social_profile_picture": u_info["picture"],
                "nickname": u_info["name"],
                "email": u_info["email"],
                "phone": None,
            },
        }
    else:
        login_data = {
            "github": {
                "social_id": u_info["id"],
                "username": u_info["bio"],
                "social_profile_picture": u_info["avatar_url"],
                "nickname": u_info["login"],
                "email": u_info["email"],
                "phone": None,
            },
        }
    user_info = login_data[service_name]
    if get_user_model().objects.filter(social_id=user_info["social_id"]).exists():
        user = get_user_model().objects.get(social_id=user_info["social_id"])
        user.token = access_token
        user.save()
    else:
        user = get_user_model()()
        user.social_id = user_info["social_id"]
        user.username = user_info["username"]
        user.social_profile_picture = user_info["social_profile_picture"]
        user.nickname = user_info["nickname"]
        # user.email = user_info["email"]
        user.phone = user_info["phone"]
        user.token = access_token
        user.set_password(str(state_token))
        user.save()
        user = get_user_model().objects.get(social_id=user_info["social_id"])
    user_login(request, user)
    return redirect(request.GET.get("next") or "accounts:test")


# test용도
def index(request):
    persons = get_user_model().objects.order_by("-pk")
    return render(
        request,
        "accounts/index.html",
        {
            "persons": persons,
        },
    )


def detail(request, user_pk):
    studys = Study.objects.order_by("-pk")
    person = get_object_or_404(get_user_model(), pk=user_pk)
    return render(
        request,
        "accounts/detail.html",
        {
            "person": person,
            "studys" : studys,
        },
    )