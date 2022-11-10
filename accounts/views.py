import secrets
import requests
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# 소셜 로그인에 필요한 토큰 생성
state_token = secrets.token_urlsafe(16)

# Create your views here.
def signup(request):
    if request.method == "POST":
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            phone = user.phone
            p1 = "".join(phone[:3])
            p2 = "".join(phone[3:7])
            p3 = "".join(phone[7:])
            phone = "-".join([p1, p2, p3])
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


def kakao_request(request):
    kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
    redirect_uri = "http://localhost:8000/accounts/login/kakao/callback"
    client_id = "9d90b5b2d651fe7e6adf2c2e261aaad3"  # 배포시 보안적용 해야함
    return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


def kakao_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "9d90b5b2d651fe7e6adf2c2e261aaad3",  # 배포시 보안적용 해야함
        "redirect_uri": "http://localhost:8000/accounts/login/kakao/callback",
        "code": request.GET.get("code"),
    }
    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    access_token = requests.post(kakao_token_api, data=data).json()["access_token"]

    headers = {"Authorization": f"bearer ${access_token}"}
    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    kakao_user_information = requests.get(kakao_user_api, headers=headers).json()
    print(kakao_user_information)  # 디버그용 코드 : 발견시 삭제 바람

    kakao_id = kakao_user_information["id"]
    kakao_nickname = kakao_user_information["properties"]["nickname"]
    kakao_profile_image = kakao_user_information["properties"]["profile_image"]

    if get_user_model().objects.filter(kakao_id=kakao_id).exists():
        kakao_user = get_user_model().objects.get(kakao_id=kakao_id)
    else:
        kakao_login_user = get_user_model()()
        kakao_login_user.username = kakao_nickname
        kakao_login_user.kakao_id = kakao_id
        if kakao_profile_image:
            kakao_login_user.social_profile_picture = kakao_profile_image
        kakao_login_user.set_password(str(state_token))
        kakao_login_user.save()
        kakao_user = get_user_model().objects.get(kakao_id=kakao_id)
    user_login(request, kakao_user)
    return redirect(request.GET.get("next") or "main:index")


def naver_request(request):
    naver_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
    client_id = "I9ScPHTpJ9smDz9KyjoX"  # 배포시 보안적용 해야함
    redirect_uri = "http://localhost:8000/accounts/login/naver/callback"
    state_token = secrets.token_urlsafe(16)
    return redirect(
        f"{naver_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state_token}"
    )


def naver_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "I9ScPHTpJ9smDz9KyjoX",  # 배포시 보안적용 해야함
        "client_secret": "4QJHVHKrOp",  # 배포시 보안적용 해야함
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "redirect_uri": "http://localhost:8000/accounts/login/naver/callback",
    }
    naver_token_request_url = "https://nid.naver.com/oauth2.0/token"
    access_token = requests.post(naver_token_request_url, data=data).json()[
        "access_token"
    ]

    headers = {"Authorization": f"bearer {access_token}"}
    naver_call_user_api = "https://openapi.naver.com/v1/nid/me"
    naver_user_information = requests.get(naver_call_user_api, headers=headers).json()
    print(naver_user_information)  # 디버그용 코드 : 발견시 삭제 바람

    naver_id = naver_user_information["response"]["id"]
    naver_nickname = naver_user_information["response"]["nickname"]
    naver_profile_image = naver_user_information["response"]["profile_image"]

    if get_user_model().objects.filter(naver_id=naver_id).exists():
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    else:
        naver_login_user = get_user_model()()
        naver_login_user.username = naver_nickname
        naver_login_user.naver_id = naver_id
        if naver_profile_image:
            naver_login_user.social_profile_picture = naver_profile_image
        naver_login_user.set_password(str(state_token))
        naver_login_user.save()
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    user_login(request, naver_user)
    return redirect(request.GET.get("next") or "main:index")


def google_request(request):
    google_api = "https://accounts.google.com/o/oauth2/v2/auth"
    client_id = "925373116590-t4uf2ra8bkt25vegkjoskvi6054hd27u.apps.googleusercontent.com"  # 배포시 보안적용 해야함
    redirect_uri = "http://localhost:8000/accounts/login/google/callback"
    google_base_url = "https://www.googleapis.com/auth"
    google_email = "/userinfo.email"
    google_myinfo = "/userinfo.profile"
    scope = f"{google_base_url}{google_email}+{google_base_url}{google_myinfo}"
    return redirect(
        f"{google_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )


def google_callback(request):
    data = {
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "grant_type": "authorization_code",
        "client_id": "925373116590-t4uf2ra8bkt25vegkjoskvi6054hd27u.apps.googleusercontent.com",  # 배포시 보안적용 해야함
        "client_secret": "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",
        "redirect_uri": "http://localhost:8000/accounts/login/google/callback",
    }
    google_token_request_url = "https://oauth2.googleapis.com/token"
    access_token = requests.post(google_token_request_url, data=data).json()[
        "access_token"
    ]
    params = {
        "access_token": f"{access_token}",
    }
    google_call_user_api = "https://www.googleapis.com/oauth2/v3/userinfo"
    google_user_information = requests.get(google_call_user_api, params=params).json()
    print(google_user_information)  # 디버그용 코드 : 발견시 삭제 바람

    googld_id = google_user_information["sub"]
    googld_name = google_user_information["name"]
    googld_email = google_user_information["email"]
    googld_picture = google_user_information["picture"]
    if get_user_model().objects.filter(googld_id=googld_id).exists():
        google_user = get_user_model().objects.get(googld_id=googld_id)
    else:
        google_login_user = get_user_model()()
        google_login_user.username = googld_name
        google_login_user.email = googld_email
        if googld_picture:
            google_login_user.social_profile_picture = googld_picture
        google_login_user.googld_id = googld_id
        google_login_user.set_password(str(state_token))
        google_login_user.save()
        google_user = get_user_model().objects.get(googld_id=googld_id)
    user_login(request, google_user)
    return redirect(request.GET.get("next") or "main:index")


def github_request(request):
    github_api = "https://github.com/login/oauth/authorize"
    client_id = "481bbe1d16187fdb9f0e"  # 배포시 보안적용 해야함
    redirect_uri = "http://localhost:8000/accounts/login/github/callback"
    scope = "read:user user:email"
    state_token = secrets.token_urlsafe(16)
    return redirect(
        f"{github_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state_token}&scope={scope}"
    )


def github_callback(request):
    data = {
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "client_id": "481bbe1d16187fdb9f0e",  # 배포시 보안적용 해야함
        "client_secret": "aaf7c5464bab25ff7a703f02a51b68803031fde3",  # 배포시 보안적용 해야함
        "redirect_uri": "http://localhost:8000/accounts/login/google/callback",
    }
    github_token_request_url = "https://github.com/login/oauth/access_token"
    access_token = requests.post(github_token_request_url, data=data).json()[
        "access_token"
    ]

    headers = {"Authorization": f"bearer ${access_token}"}
    github_user_api = "https://api.github.com/user"
    github_user_information = requests.get(github_user_api, headers=headers).json()
    print(github_user_information)  # 디버그용 코드 : 발견시 삭제 바람

    github_id = github_user_information["sub"]
    github_name = github_user_information["name"]
    github_email = github_user_information["email"]
    github_picture = github_user_information["picture"]
    if get_user_model().objects.filter(github_id=github_id).exists():
        github_user = get_user_model().objects.get(github_id=github_id)
    else:
        github_login_user = get_user_model()()
        github_login_user.username = github_name
        if github_email:
            github_login_user.email = github_email
        if github_picture:
            github_login_user.social_profile_picture = github_picture
        github_login_user.github_id = github_id
        github_login_user.set_password(str(state_token))
        github_login_user.save()
        github_user = get_user_model().objects.get(github_id=github_id)
    user_login(request, github_user)
    return redirect(request.GET.get("next") or "main:index")
