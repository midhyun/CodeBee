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
            'categorie',
            'study_type',
            'location_type',
            'location',
            'image',
            'deadline'
        ]
        labels = {
            'title': "스터디명",
            'limits': '최대 참여',
            'tag': '태그',
            'content': '규칙 및 소개',
            'categorie': '공부과목',
            'study_type': '진행방법',
            'location_type': '모임형태',
            'location': '장소',
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