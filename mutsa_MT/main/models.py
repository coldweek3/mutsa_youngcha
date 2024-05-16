from django.db import models
import random

class Mission(models.Model):
    description = models.CharField(max_length=200)
    is_assigned = models.BooleanField(default=False)

    def __str__(self):
        return self.description

    @classmethod
    def assign_random(cls):
        unassigned_missions = cls.objects.filter(is_assigned=False)
        if unassigned_missions:
            return random.choice(unassigned_missions)
        return None

class Lion(models.Model):
    name = models.CharField(max_length=3, unique=True)
    password = models.CharField(max_length=4, blank=True, null=True)
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
