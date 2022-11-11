from django import forms
from .models import Study, Accepted

LOCATION_TYPE_CHOICE = (
    ('false', '오프라인'),
    ('true', '온라인')
)

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = [
            'title',
            'limits',
            'tag',
            'content',
            'image',
            'deadline'
        ]
        labels = {
            'title': "스터디명",
            'limits': '최대 참여',
            'tag': '태그',
            'content': '규칙 및 소개',
            'image': '이미지',
            'deadline': '모집 마감일',
        }
        widgets = {
            'location_type': forms.Select(choices=LOCATION_TYPE_CHOICE)
        }

class AcceptedForm(forms.ModelForm):
    class Meta:
        model = Accepted
        fields = ['joined']