from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudyForm, CommentForm, AcceptedForm
from .models import Study, Comment, Accepted
from accounts.models import User
import requests
import json

# Create your views here.

def home(request):
    return render(request, 'home.html')


def index(request):
    studies = Study.objects.order_by('-pk')
    context = {
        'studies': studies,
    }
    return render(request, 'reviews/index.html', context)



def create(request):
    if request.method == 'POST':
        study_form = StudyForm(request.POST, request.FILES)
        print(request.POST)
        if study_form.is_valid():
            study = study_form.save(commit=False)
            study.categorie = request.POST['categorie']
            study.study_type = request.POST['study_type']
            study.location_type = request.POST['location_type']
            study.location = request.POST['location']
            study.X = request.POST['X']
            study.Y = request.POST['Y']
            study.host = request.user
            study.deadline = request.POST['deadline']
            study.save()
            Aform = Accepted(joined=True, study=study, users=study.host)
            Aform.save()
            return redirect('reviews:index')
    else:
        study_form = StudyForm()
    context = {'study_form': study_form}
    return render(request, 'reviews/form.html', context)


def detail(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    cnt = len(Accepted.objects.filter(study=study))
    context = {'study' : study,
               'cnt':cnt}
    return render(request,'reviews/detail.html', context)



def userlist(request, study_pk):
    users = Accepted.objects.filter(study_id=study_pk)
    study = Study.objects.filter(pk=study_pk)
    context = {
        'members': users,
        'study': Study.objects.get(pk=study_pk),
    }
    return render(request, 'reviews/userlist.html', context)


def update(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    if request.user == study.host:
        if request.method == 'POST':
            study_form = StudyForm(request.POST, request.FILES, instance=study)
            if study_form.is_valid():
                study = study_form.save(commit=False)
                study.categorie = request.POST['categorie']
                study.study_type = request.POST['study_type']
                study.location_type = request.POST['location_type']
                study.location = request.POST['location']
                study.X = request.POST['X']
                study.Y = request.POST['Y']
                study.deadline = request.POST['deadline']
                study.host = request.user
                study.save()
                study_form.save()
                return redirect('reviews:detail', study_pk)
        else:
            study_form = StudyForm(instance=study)
        context = {'study_form': study_form}
        return render(request, 'reviews/form.html', context)
    else:
        return redirect('reviews:detail', study_pk)


def delete(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    study.delete()
    return redirect('reviews:index')



def join(request, study_pk, user_pk):
    study = Study.objects.get(pk=study_pk)
    accepted = Accepted.objects.filter(study_id=study_pk)
    users = Accepted.objects.filter(users_id=user_pk)
    print(users)
    if study.limits > len(accepted):
        for joined in users:
            if joined in accepted:
                print('이미 가입되어 있습니다.')
                return redirect('reviews:detail', study_pk)
        else:
            Aform = Accepted(joined=False,study=study,users=request.user)
            Aform.save()
            print('가입 신청')
            return redirect('reviews:detail', study_pk)
    else:
        return redirect('reviews:detail', study_pk)

def study_accepted(request, study_id, users_id):
    study = Study.objects.get(id=study_id)
    user = User.objects.get(id=users_id)
    aform = Accepted.objects.get(users=user, study=study)
    if request.user == study.host:
        aform.joined = True
        aform.save()
        return redirect('reviews:userlist', study_id)
    else:
        return redirect('reviews:userlist', study_id)


def study_kick(request, study_id, users_id):
    study = Study.objects.get(id=study_id)
    user = User.objects.get(id=users_id)
    aform = Accepted.objects.get(users=user, study=study)
    if request.user == study.host and user != study.host:
        aform.delete()
        return redirect('reviews:userlist', study_id)
    elif request.user == user and user != study.host:
        aform.delete()
        return redirect('reviews:index')
    else:
        return redirect('reviews:userlist', study_id)

url="https://kapi.kakao.com/v2/api/talk/memo/default/send"




def gathering(request, study_pk):
    accepted = Accepted.objects.filter(study_id=study_pk, joined=1)
    data={
    "template_object": json.dumps({
        "object_type":"text",
        "text":"요원이 거의 모였어요 준비하세요!",
        "link":{
            "web_url":"www.naver.com",
            "mobile_url":"www.naver.com"
        }})}
    for user in accepted:
        token = user.users.token
        if token:
            headers={"Authorization" : "Bearer " + token}
            response = requests.post(url, headers=headers, data=data)
            print(str(response.json()))
        else:
            print('no')
    return redirect('reviews:detail', study_pk)
# ==================================comment=======================
def review(request, study_id):
    study = Study.objects.get(pk=study_id)
    comments = Comment.objects.all().order_by('-pk')
    comment_form = CommentForm()
    context = {
        'review': study,
        'comment_form' : comment_form,
        'comments': comments,
    }

    return render(request, 'reviews/review.html', context)


def comment_create(request, pk):
    review = get_object_or_404(Study, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        print(review.id)
        comment.study_id = review.id
        comment.user = request.user

        comment.save()

        comments = Comment.objects.filter(study_id=pk).order_by('-pk')
        comments_data = []
        for co in comments:
            co.created_at = co.created_at.strftime('%Y-%m-%d %H:%M')
            comments_data.append(
                {
                    'request_user_pk': request.user.pk,
                    'comment_pk': co.pk,
                    'user_pk': co.user.pk,
                    'username': co.user.username,
                    'content': co.content,
                    'created_at': co.created_at,
                    'updated_at': co.updated_at,
                    'study_id': co.study_id,
                })
        context = {
            'comments_data': comments_data
        }
        return JsonResponse(context)


def comment_update(request, pk, comment_pk):
    if request.user.is_authenticated:
        jsonObject = json.loads(request.body)

        comment = Comment.objects.get(pk=comment_pk)
        comment.comment_content = jsonObject.get('content')
        comment.save()

        comments = Comment.objects.filter(study_id=pk).order_by('-pk')
        comments_data = []
        for co in comments:
            co.created_at = co.created_at.strftime('%Y-%m-%d %H:%M')
            comments_data.append(
                {
                    'request_user_pk': request.user.pk,
                    'comment_pk': co.pk,
                    'user_pk': co.user.pk,
                    'username': co.user.username,
                    'content': co.content,
                    'created_at': co.created_at,
                    'updated_at': co.updated_at,
                    'study_id': co.study_id,
                })
        context = {
            'comments_data': comments_data
        }
        return JsonResponse(context)


def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()

        comments = Comment.objects.filter(study_id=pk).order_by('-pk')
        comments_data = []
        for co in comments:
            co.created_at = co.created_at.strftime('%Y-%m-%d %H:%M')
            comments_data.append(
                {'request_user_pk': request.user.pk,
                 'comment_pk': co.pk,
                 'user_pk': co.user.pk,
                 'username': co.user.username,
                 'content': co.content,
                 'created_at': co.created_at,
                 'updated_at': co.updated_at,
                 'study_id': co.study_id,
                 })
        context = {
            'comments_data': comments_data
        }
        return JsonResponse(context)