from django import forms
from .models import Review,Study, Accepted


LOCATION_TYPE_CHOICE = (
    ('false', '오프라인'),
    ('true', '온라인')
)
STUDY_TYPE_CHOICE =(
    ('장기', '그룹(주기적인 활동)'),
    ('단기', '당일(1회성)')
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
            'deadline',
        ]
        labels = {
            'title': "스터디명",
            'limits': '최대 참여',
            'tag': '태그',
            'content': '스터디 주제',
            'image': '이미지',
            'deadline': '모집 마감일',
        }
        widgets = {
            'location_type': forms.Select(choices=LOCATION_TYPE_CHOICE),
            'study_type' : forms.Select(choices=STUDY_TYPE_CHOICE),
        }

class AcceptedForm(forms.ModelForm):
    class Meta:
        model = Accepted
        fields = ['joined']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = (
            "review",
            "user",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget.attrs = {
            "placeholder": "댓글을 작성해 주세요",
        }
        self.fields["content"].help_text = None
