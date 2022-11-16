from django import forms
from .models import Comment,Study, Accepted, Honey


LOCATION_TYPE_CHOICE = (
    ('false', '오프라인'),
    ('true', '온라인')
)
STUDY_TYPE_CHOICE =(
    ('그룹 스터디', '그룹 스터디'),
    ('당일 스터디', '당일 스터디')
)

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = [
            'title',
            'limits',
            'content',
            'image',
        ]
        labels = {
            'title': "스터디명",
            'limits': '최대 참여',
            'content': '스터디 소개',
            'image': '이미지',
        }
        widgets = {
            'location_type': forms.Select(choices=LOCATION_TYPE_CHOICE),
            'study_type': forms.Select(choices=STUDY_TYPE_CHOICE),
        }

class AcceptedForm(forms.ModelForm):
    class Meta:
        model = Accepted
        fields = ['joined']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'comment_content': '',
        }
        widgets = {
            'comment_content': forms.TextInput(attrs={'placeholder': '댓글작성', 'style': 'width:400px;'}),
        }

class HoneyForm(forms.ModelForm):
    class Meta:
        model = Honey
        fields = ['like', 'dislike']