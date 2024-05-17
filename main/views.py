from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lion, Mission, Quiz
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
                    # messages.error(request, "비밀번호가 틀렸다옹")
                    request.session['error_message'] = "비밀번호가 틀렸다옹"
            else:
                if len(password) == 4 and password.isdigit():
                    lion.password = password  # 비밀번호 설정
                    lion.save()
                    request.session['lion_id'] = lion.id
                    return redirect('missionPage')
                else:
                    # messages.error(request, "비밀번호는 숫자 4자리라옹") 
                    request.session['error_message'] = "비밀번호는 숫자 4자리라옹" # 비밀번호 유효성 검사 실패
        except Lion.DoesNotExist:
            # messages.error(request, "당신은 동멋 라이옹이 아니군요!")
            request.session['error_message'] = "당신은 동멋 MT 참가자 라이옹이 아니군요!"  # DB에 이름이 없는 경우

    message = request.session.pop('error_message', None)
    return render(request, 'main/firstPage.html', {
        'message': message
    })

def missionPage(request):
    lion_id = request.session.get('lion_id')
    if not lion_id:
        return redirect('firstPage')
    lion = Lion.objects.get(id=lion_id)

    # 세션에서 메시지 가져오기
    message = request.session.pop('error_message', None)

    return render(request, 'main/mission.html', {
        'lion': lion,
        'mission': lion.mission,
        'message': message  # 템플릿에 메시지 전달
    })

def changeMissionPage(request):
    lion_id = request.session.get('lion_id')
    if not lion_id:
        return redirect('firstPage')
    lion = Lion.objects.get(id=lion_id)

    # 사용자가 이미 미션을 변경했는지 확인
    if lion.mission_changes >= 1:  # 한 번 변경했다면 다시 변경할 수 없음
        return redirect('missionPage')

    if lion.quiz_attempted == 1:  # 한 번 변경했다면 다시 변경할 수 없음
        return redirect('missionPage')

    # 미션 변경 페이지로 리디렉트
    return render(request, 'main/changeMission.html', {
        'lion': lion
    })

def quizPage(request):
    if request.method == "POST":
        user_answer = request.POST.get('user_answer')
        quiz = Quiz.objects.first()  # 첫 번째 퀴즈를 가져옴

        lion = Lion.objects.get(id=request.session['lion_id'])
        lion.quiz_attempted = True  # 퀴즈 시도 표시
        lion.save()

        if user_answer == quiz.answer:
            # message = "정답입니다!! 과연 당신의 미션은?"
            request.session['error_message'] = "정답입니다!! 과연 당신의 미션은?"
            lion = Lion.objects.get(id=request.session['lion_id'])
            new_mission = Mission.assign_random()
            lion.mission = new_mission
            new_mission.is_assigned = True
            new_mission.save()
            lion.mission_changes += 1  # 미션 변경 횟수 1 증가
            lion.save()
        else:
            request.session['error_message'] = "땡!!!!"

        # messages.info(request, message)
        return redirect('missionPage')

    quiz = Quiz.objects.first()  # 첫 번째 퀴즈를 로드
    return render(request, 'main/quizPage.html', {'quiz': quiz})

# def assign_mission_to_lion(request):
#     lion_id = request.session.get('lion_id')
#     if not lion_id:
#         return redirect('login')
#     lion = Lion.objects.get(id=lion_id)
#     mission = Mission.assign_random()
#     if mission:
#         lion.mission = mission
#         mission.assigned_count += 1
#         mission.save()
#         lion.save()
#         messages.success(request, "새로운 미션을 할당받았습니다.")
#     else:
#         messages.error(request, "할당 가능한 미션 없음")
#     return redirect('some_view')
