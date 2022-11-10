from django.db import models
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator


def input_only_number(value):
    if not value.isdigit():
        raise ValidationError("숫자만 적을 수 있습니다.")


# Create your models here.
class User(AbstractUser):
    kakao_id = models.BigIntegerField(null=True, unique=True)
    naver_id = models.CharField(null=True, unique=True, max_length=100)
    googld_id = models.CharField(null=True, unique=True, max_length=50)
    github_id = models.CharField(null=True, unique=True, max_length=100)
    profile_picture = ProcessedImageField(
        upload_to="profile_pictures/",
        blank=True,
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
    )
    # 닉네임 20자 제한
    nickname = models.CharField(max_length=20)
    location = models.CharField(max_length=100, blank=True)

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"
