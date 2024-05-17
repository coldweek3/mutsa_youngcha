from django.db import models
import random

class Mission(models.Model):
    description = models.CharField(max_length=200)
    is_assigned = models.BooleanField(default=False)
    assigned_count = models.IntegerField(default=0)  # 미션을 받은 사용자 수를 추적

    def __str__(self):
        return self.description

    @classmethod
    def assign_random(cls):
        # 할당 가능한 미션은 최대 3명까지만 받을 수 있도록 조정
        possible_missions = cls.objects.filter(assigned_count__lt=3)
        if possible_missions:
            return random.choice(possible_missions)
        return None

class Lion(models.Model):
    name = models.CharField(max_length=3, unique=True)
    password = models.CharField(max_length=4, blank=True, null=True)
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True)
    mission_changes = models.IntegerField(default=0) # 미션 변경 횟수(한 번으로 제한!)
    quiz_attempted = models.BooleanField(default=False)  # 퀴즈 시도 여부

    def __str__(self):
        return self.name
    
class Quiz(models.Model):
    question = models.CharField(max_length=255)  # 퀴즈 문제
    answer = models.CharField(max_length=255)  # 퀴즈 정답

    def __str__(self):
        return f"Question: {self.question} - Answer: {self.answer}"