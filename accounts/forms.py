from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "last_name",
            "first_name",
            "email",
            "phone",
            "nickname",
        )
        labels = {
            "nickname": "닉네임",
            "phone": "핸드폰 번호",
        }
        widgets = {
            "nickname": forms.TextInput(
                attrs={
                    "placeholder": "닉네임",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "성",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "이름",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "'-' 를 제외하고 입력해주세요.",
                    "style": "width: 100%; resize: none;",
                }
            ),
        }
