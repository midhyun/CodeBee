from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "fullname",
            "nickname",
            "phone",
            "email",
            "profile_picture",
        )
        labels = {
            "fullname": "이름",
            "nickname": "닉네임",
            "phone": "핸드폰 번호",
            "email": "이메일",
            "profile_picture": "프로필 사진",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "아이디는 16자 이내로 적어주세요.",
                }
            ),
            "nickname": forms.TextInput(
                attrs={
                    "placeholder": "닉네임을 입력해주세요.",
                }
            ),
            "fullname": forms.TextInput(
                attrs={
                    "placeholder": "본명을 입력해주세요.",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "'-' 를 제외하고 입력해주세요.",
                    "style": "width: 100%; resize: none;",
                }
            ),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        exclude = ("password",)
        fields = (
            "nickname",
            "profile_picture",
        )
        labels = {
            "nickname": "닉네임",
        }
        widgets = {
            "nickname": forms.TextInput(
                attrs={
                    "placeholder": "닉네임을 입력해주세요.",
                }
            ),
        }


class LocationChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "location",
            "detail_location",
        )
        labels = {
            "location": "",
            "detail_location": "",
        }
        widgets = {
            "location": forms.TextInput(
                attrs={
                    "placeholder": "주소",
                }
            ),
            "detail_location": forms.TextInput(
                attrs={
                    "placeholder": "상세주소",
                }
            ),
        }


class AuthForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "phone",
            "email",
        )
        labels = {
            "phone": "핸드폰 번호",
            "email": "이메일",
        }
        widgets = {
            "email": forms.TextInput(
                attrs={
                    "placeholder": "이메일을 입력해주세요.",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "'-' 를 제외하고 입력해주세요.",
                    "style": "width: 100%; resize: none;",
                }
            ),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")
        if old_password == new_password1:
            raise forms.ValidationError("이전 비밀번호와 새 비밀번호가 같습니다.")
        return new_password1
