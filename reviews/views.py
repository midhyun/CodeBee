from django.shortcuts import render,redirect
from .forms import StudyForm, ReviewForm,AcceptedForm
from .models import Study,Review,Accepted
from accounts.models import User
import requests
import json
from django.contrib import messages
# Create your views here.
# 카카오톡 나에게 보내기 메시지 url
url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

def home(request):
    return render(request, 'home.html')

def index(request):
    studies = Study.objects.order_by('-pk')
    context = {
        'studies': studies
    }
    return render(request, 'reviews/index.html', context)

def create(request):
    print(request.POST)
    if request.method =='POST':
        study_form = StudyForm(request.POST, request.FILES)
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
            Aform = Accepted(joined=True,study=study,users=study.host)
            Aform.save()
            return redirect('reviews:index')
    else:
        study_form = StudyForm()
    context = {'study_form' : study_form}
    return render(request, 'reviews/form.html', context)

def detail(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    review_form = ReviewForm()
    context = {'study' : study,
               'review_form': review_form}
    return render(request,'reviews/detail.html', context)

def userlist(request, study_pk):
    users = Accepted.objects.filter(study_id=study_pk)
    study = Study.objects.filter(pk=study_pk)
    context = {
        'members':users,
        'study':Study.objects.get(pk=study_pk),
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
    token = study.host.token
    if study.limits > len(accepted):
        for joined in users:
            if joined in accepted:
                messages.warning(request, '이미 가입신청 한 그룹입니다.')
                return redirect('reviews:detail', study_pk)
        else:
            Aform = Accepted(joined=False,study=study,users=request.user)
            Aform.save()
            try: image_url = study.image.url
            except: image_url = ''
            data = {"template_object": json.dumps({
            "object_type": "feed",
            "content": {
                "title": f"{request.user}님의 스터디 가입신청! ({len(accepted)} / {study.limits})",
                "description": "신청을 승인해주세요!",
                "image_url": f"https://user-images.githubusercontent.com/108651809/201609398-060cbab1-1ff4-440f-a989-9ab77965eb94.png",
                # "image_url": f"http://localhost:8000{image_url}",
                "image_width": 800,
                "image_height": 563,
                "link": {
                    "web_url": "http://localhost:8000",
                    "mobile_web_url": "http://localhost:8000",
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            },
            "buttons": [
                {
                    "title": "웹으로 이동",
                    "link": {
                        "web_url": "http://localhost:8000",
                        "mobile_web_url": "http://localhost:8000"
                    }
                },
                {
                    "title": "앱으로 이동",
                    "link": {
                        "android_execution_params": "contentId=100",
                        "ios_execution_params": "contentId=100"
                    }
                }
            ]
            })}
            headers={"Authorization" : "Bearer " + token}
            response = requests.post(url, headers=headers, data=data)
            print(str(response.json()))
            messages.success(request, '가입 신청이 완료되었습니다. 호스트의 승인을 기다려 주세요.')
            return redirect('reviews:detail', study_pk)
    else:
        messages.success(request, '모집인원이 가득 찬 그룹입니다.')
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


def gathering(request, study_pk):
    accepted = Accepted.objects.filter(study_id=study_pk, joined=1)
    study = Study.objects.get(pk=study_pk)
    message = request.POST["message"]
    try: image_url = study.image.url
    except: image_url = ''
    data = {"template_object": json.dumps({
            "object_type": "feed",
            "content": {
                "title": f"{request.user}님의 메시지",
                "description": f"{message}",
                "image_url": f"https://user-images.githubusercontent.com/108651809/201609398-060cbab1-1ff4-440f-a989-9ab77965eb94.png",
                # "image_url": f"http://localhost:8000{image_url}",
                "image_width": 800,
                "image_height": 550,
                "link": {
                    "web_url": "http://localhost:8000",
                    "mobile_web_url": "http://localhost:8000",
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            },
            "buttons": [
                {
                    "title": "웹으로 이동",
                    "link": {
                        "web_url": "http://localhost:8000",
                        "mobile_web_url": "http://localhost:8000"
                    }
                },
                {
                    "title": "앱으로 이동",
                    "link": {
                        "android_execution_params": "contentId=100",
                        "ios_execution_params": "contentId=100"
                    }
                }
            ]
            })}
    for user in accepted:
        token = user.users.token
        if token:
            headers={"Authorization" : "Bearer " + token}
            response = requests.post(url, headers=headers, data=data)
            print(str(response.json()))
            messages.success(request, '메시지 전송이 완료되었습니다.')
        else:
            print('no')
            pass
    
    return redirect('reviews:detail', study_pk)