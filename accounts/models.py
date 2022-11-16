import os
import time
import hmac
import base64
import hashlib
import requests
from django.db import models
from dotenv import load_dotenv
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator


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
        unique=True,
        max_length=16,
        validators=[UnicodeUsernameValidator()],
        verbose_name="아이디",
    )
    nickname = models.CharField(max_length=20, blank=True)
    phone = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(11), MaxLengthValidator(11), input_only_number],
        blank=True,
        null=True,
    )
    fullname = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=30)
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
    # 소셜 아이디 관련 필드
    git_username = models.CharField(null=True, blank=True, max_length=50)
    boj_username = models.CharField(null=True, blank=True, max_length=50)
    social_id = models.CharField(null=True, max_length=100)
    is_social_account = models.BooleanField(default=False)
    social_profile_picture = models.CharField(
        null=True, max_length=150
    )  # >>> url 형식으로 받아와야 함
    is_phone_active = models.BooleanField(default=False)
    is_email_active = models.BooleanField(default=False)
    token = models.CharField(max_length=150, null=True, blank=True)


load_dotenv()


class AuthPhone(TimeStampedModel):
    phone = models.IntegerField()
    auth_number = models.IntegerField()

    NAVER_CLOUD_ACCESS_KEY = os.getenv("NAVER_CLOUD_ACCESS_KEY")
    NAVER_CLOUD_SECRET_KEY = os.getenv("NAVER_CLOUD_SECRET_KEY")
    NAVER_CLOUD_SERVICE_ID = os.getenv("NAVER_CLOUD_SERVICE_ID")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_sms()

    def send_sms(self):
        timestamp = str(int(time.time() * 1000))
        access_key = self.NAVER_CLOUD_ACCESS_KEY
        secret_key = bytes(self.NAVER_CLOUD_SECRET_KEY, "UTF-8")
        service_id = self.NAVER_CLOUD_SERVICE_ID
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
