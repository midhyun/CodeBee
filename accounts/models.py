from django.db import models
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator


def input_only_number(value):
    if not value.isdigit():
        raise ValidationError("숫자만 적을 수 있습니다.")


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = models.CharField(
        error_messages={"unique": "같은 아이디가 이미 존재합니다."},
        max_length=16,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name="아이디",
    )
    fullname = models.CharField(max_length=20, blank=True)
    phone = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(11), MaxLengthValidator(11), input_only_number],
        blank=True,
        null=True,
    )
    nickname = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    detail_location = models.CharField(max_length=30, blank=True)
    profile_picture = ProcessedImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        processors=[ResizeToFill(128, 128)],
        format="JPEG",
        options={
            "quality": 30,
        },
    )
    # url 형식으로 받아와야 함
    social_profile_picture = models.CharField(null=True, max_length=150)
    phone = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(11), MaxLengthValidator(11), input_only_number],
        blank=True,
        null=True,
    )
    likes = models.ManyToManyField("self", symmetrical=False, related_name="ls")
    dislikes = models.ManyToManyField("self", symmetrical=False, related_name="ds")
    # 닉네임 20자 제한
    nickname = models.CharField(max_length=20)
    location = models.CharField(max_length=100, blank=True)
    # 소셜 아이디 관련 필드
    social_id = models.CharField(null=True, max_length=100)
    is_social_account = models.BooleanField(default=False)
    social_profile_picture = models.CharField(
        null=True, max_length=150
    )  # >>> url 형식으로 받아와야 함
    is_phone_active = models.BooleanField(default=False)
    is_email_active = models.BooleanField(default=False)
    token = models.CharField(max_length=150, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"


import time
import hmac
import base64
import hashlib
import requests


class AuthPhone(TimeStampedModel):
    phone = models.IntegerField()
    auth_number = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_sms()

    def send_sms(self):
        timestamp = str(int(time.time() * 1000))
        access_key = "uuLXZ69D3OHR1C98uyyF"  # 배포시 보안 적용 필수
        secret_key = "VlJmCGao0WOsJ9oPl8u3C2esuK6s6wmrdRqAImR7"  # 배포시 보안 적용 필수
        secret_key = bytes(secret_key, "UTF-8")
        service_id = "ncp:sms:kr:295990079948:codebee"  # 배포시 보안 적용 필수
        method = "POST"
        uri = f"/sms/v2/services/{service_id}/messages"
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, "UTF-8")
        signing_key = base64.b64encode(
            hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
        )
        url = f"https://sens.apigw.ntruss.com/sms/v2/services/{service_id}/messages"
        data = {
            "type": "SMS",
            "from": "01099453849",
            "content": f"[코드비] 인증 번호 [{self.auth_number}]를 입력해주세요.",
            "messages": [{"to": f"{self.phone}"}],
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signing_key,
        }
        # 여기서 인증번호가 보내짐
        requests.post(url, json=data, headers=headers)
