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
            "email",
            "phone",
            "git_username",
            "boj_username",
            "profile_picture",
        )
        labels = {
            "fullname": "이름",
            "nickname": "닉네임",
            "email": "이메일",
            "phone": "휴대폰 번호",
            "git_username": "깃허브 아이디",
            "boj_username": "백준 아이디",
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
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "'-' 를 제외하고 입력해주세요.",
                    "style": "width: 100%; resize: none;",
                }
            ),
            "git_username": forms.TextInput(
                attrs={
                    "placeholder": "깃허브 아이디는 깃허브 사용 언어 통계에 사용됩니다.",
                }
            ),
            "boj_username": forms.TextInput(
                attrs={
                    "placeholder": "아이디가 이메일 형식일 경우 이메일 부분을 뺀 아이디만 입력해주세요.",
                }
            ),
            "fullname": forms.TextInput(
                attrs={
                    "placeholder": "본명을 입력해주세요.",
                }
            ),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "nickname",
            "git_username",
            "boj_username",
            "profile_picture",
        )
        labels = {
            "nickname": "닉네임",
            "git_username": "깃허브 아이디",
            "boj_username": "백준 아이디",
            "profile_picture": "프로필 사진",
        }
        widgets = {
            "nickname": forms.TextInput(
                attrs={
                    "placeholder": "닉네임을 입력해주세요.",
                }
            ),
            "git_username": forms.TextInput(
                attrs={
                    "placeholder": "깃허브 아이디는 깃허브 사용 언어 통계에 사용됩니다.",
                }
            ),
            "boj_username": forms.TextInput(
                attrs={
                    "placeholder": "백준 아이디를 입력하시면 프로필에 백준 티어가 나옵니다.",
                }
            ),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "address",
            "detail_address",
        )
        labels = {
            "address": "",
            "detail_address": "",
        }
        widgets = {
            "address": forms.TextInput(
                attrs={
                    "placeholder": "주소",
                }
            ),
            "detail_address": forms.TextInput(
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
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "'-' 를 제외하고 입력해주세요.",
                    "style": "width: 100%; resize: none;",
                }
            ),
        }


class SNSUserSignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "social_id",
            "service_name",
            "is_social_account",
            "token",
            "social_profile_picture",
        )
        widgets = {
            "social_id": forms.HiddenInput,
            "service_name": forms.HiddenInput,
            "is_social_account": forms.HiddenInput,
            "token": forms.HiddenInput,
            "social_profile_picture": forms.HiddenInput,
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")
        if old_password == new_password1:
            raise forms.ValidationError("이전 비밀번호와 새 비밀번호가 같습니다.")
        return new_password1
