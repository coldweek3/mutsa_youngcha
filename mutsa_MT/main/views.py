from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lion, Mission
import random

# Create your views here.
def intropage(request):
    return render(request, 'main/intro.html')

def firstPage(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')

        try:
            lion = Lion.objects.get(name=name)
            if lion.password:  # 이미 비밀번호가 설정된 경우
                if lion.password == password:
                    request.session['lion_id'] = lion.id
                    return redirect('missionPage')
                else:
                    messages.error(request, "비밀번호가 틀렸습니다.")
            else:
                if len(password) == 4 and password.isdigit():
                    lion.password = password  # 비밀번호 설정
                    lion.save()
                    request.session['lion_id'] = lion.id
                    return redirect('missionPage')
                else:
                    messages.error(request, "비밀번호는 숫자 4자리라옹")  # 비밀번호 유효성 검사 실패
        except Lion.DoesNotExist:
            messages.error(request, "당신은 동멋 라이옹이 아니군요!")  # DB에 이름이 없는 경우

    return render(request, 'main/firstPage.html')

def missionPage(request):
    lion_id = request.session.get('lion_id')
    if not lion_id:
        return redirect('firstPage')
    lion = Lion.objects.get(id=lion_id)
    if not lion.mission:
        mission = Mission.assign_random()
        if mission:
            lion.mission = mission
            mission.is_assigned = True
            mission.save()
            lion.save()

    else:
        mission = lion.mission
    return render(request, 'main/mission.html', {
            'lion': lion,
            'mission': mission
        })

def changeMissionPage(request):
    lion_id = request.session.get('lion_id')
    if not lion_id:
        return redirect('firstPage')
    lion = Lion.objects.get(id=lion_id)
    if lion.mission:
        lion.mission.is_assigned = False
        lion.mission.save()
        new_mission = Mission.assign_random()
        if new_mission:
            lion.mission = new_mission
            new_mission.is_assigned = True
            new_mission.save()
            lion.save()
    return redirect('missionPage')