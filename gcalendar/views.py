from django.shortcuts import render, redirect
import requests
# Create your views here.
def test(request):
    return render(request, 'gcalendar/test.html')

client_id = "503216611677-g9p12g4p2an35h2srqknqhg6p1s4469o.apps.googleusercontent.com"
client_secret = "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"
redirect_uri = "http://localhost:8000/gcalendar/google_code"
# 콜
def google_call(request):
    client_id = "503216611677-g9p12g4p2an35h2srqknqhg6p1s4469o.apps.googleusercontent.com"
    client_secret = "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"
    redirect_uri = "http://localhost:8000/gcalendar/google_code"
    url = f'https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&access_type=offline&prompt=consent&redirect_uri={redirect_uri}&response_type=code&scope=https://www.googleapis.com/auth/calendar'
    return redirect(url)
# 콜백
def google_code(request):
    client_id = "503216611677-g9p12g4p2an35h2srqknqhg6p1s4469o.apps.googleusercontent.com"
    client_secret = "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"
    redirect_uri = "http://localhost:8000/gcalendar/google_code"
    url = 'https://oauth2.googleapis.com/token'
    data = {
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
                "client_id": client_id,  # 배포시 보안적용 해야함
                "client_secret": client_secret,  # 배포시 보안적용 해야함
                "project_id":"keen-button-368611",
                "state": request.GET.get("state"),
                "code": request.GET.get("code"),
            }
            
    res = requests.post(url, data=data).json()
    print('call-----------------------------')
    print(res)
    token = res['access_token']
    usertoken = UserToken()
    usertoken.user = request.user
    usertoken.token = token
    re_token = res['refresh_token']
    usertoken.re_token = re_token
    usertoken.save()
    # Calendar event
    curl = 'https://www.googleapis.com/calendar/v3/calendars/primary/events?key=AIzaSyDpJRl5rjY_ntaBs09g7FqPns-9lOPnyLQ'
    cheaders = {
        "Authorization": 'Bearer' + token,
        "Accept": 'application/json',
        "Content-Type": 'application/json'
    }
    # data = {
    #     "end":{
    #         "dateTime":schedule.study_end.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "timeZone":"Asia/Seoul"
    #     },
    #     "start":{
    #         "dateTime":schedule.study_at.strftime("%Y-%m-%dT%H:%M:%S"),
    #         "timeZone":"Asia/Seoul"
    #     },
    #     "summary": study.title,
    #     "location":study.location,
    #     "description": study.content
    # }
    cdata = {
    "end":{
        "dateTime":'2022-11-20T13:00:00',
        "timeZone":"Asia/Seoul"
    },
    "start":{
        "dateTime":'2022-11-20T13:00:00',
        "timeZone":"Asia/Seoul"
    },
    "summary": '요약제목',
    "location":'서울',
    "description": '왜 자꾸 에러가 날까!'
    }

    response = requests.post(curl, headers=cheaders, data=cdata)
    if response.json().get('code') == 200:
        print('일정이 성공적으로 등록되었습니다.')
    else:
        print('일정이 성공적으로 등록되지 못했습니다. 오류메시지 : ' + str(response.json()))
        url = 'https://www.googleapis.com/oauth2/v4/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': re_token,
            'grant_type': 'refresh_token',
        }
        res = requests.post(url, headers=headers, data=data).json()
        print('refresh-----------------------------')
        print(res)
        token = res['access_token']
        cheaders = {
            "Authorization": 'Bearer'+ token,
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
        response = requests.post(curl, headers=cheaders, data=cdata)
        if response.json().get('code') == 200:
            print('리프레시 후 일정이 성공적으로 등록되었습니다.')
        else:
            print('리프레시 후 오류메시지:' + str(response.json()))
    return redirect('gcalendar:test')

def calendar_event(request):
    token = request.user.token
    url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events?key=AIzaSyDpJRl5rjY_ntaBs09g7FqPns-9lOPnyLQ'
    headers = {
        "Authorization": 'Bearer' + token,
        "Accept": 'application/json',
        "Content-Type": 'application/json'
    }
    data = {
            "end":{
        "dateTime":'2022-11-20T13:00:00',
        "timeZone":"Asia/Seoul"
        },
        "start":{
            "dateTime":'2022-11-20T13:00:00',
            "timeZone":"Asia/Seoul"
        },
        "summary": '요약제목',
        "location":'서울',
        "description": '왜 자꾸 에러가 날까!'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.json().get('code') == 200:
            print('일정이 성공적으로 등록되었습니다.')
    else:
        print('오류메시지:' + str(response.json()))
    return redirect('gcalendar:test')
