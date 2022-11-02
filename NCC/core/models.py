from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver # this decorator.
from django.conf import settings
import os

class Player(AbstractUser):
    total_score=models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.username

class Question(models.Model):
    score=models.IntegerField(null=True,default=1)
    title=models.CharField(max_length=1003, null=True)
    body = models.TextField(null=True)
    description= models.CharField(max_length=1003, null=True)
    input_format=models.TextField(null=True)
    output_format=models.TextField(null=True)  
    constraints=models.TextField(null=True)
    sample_input=models.TextField(null=True)
    sample_output=models.TextField(null=True)
    explaination=models.TextField(null=True)
    correct_submissions = models.IntegerField(null=True)
    total_submissions = models.IntegerField(null=True)
    accuracy = models.FloatField(null=True)
    time_limt=models.IntegerField(null=True,default=1)
    memory_limit = models.IntegerField(null=True,default=256)
    # questions score for junior senior.
    def __str__(self):
        return self.title


class Submission(models.Model):
    q_id = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    p_id = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    hours = models.IntegerField(null=True,default=0)
    mins = models.IntegerField(null=True,default=0)
    code = models.TextField(null=True)  # text field
    status = models.CharField(
        max_length=20,
        null=True,
        choices=(
            ("WA", "Wrong Answer"),
            ("AC", "Accepted"),
            ("TLE", "Time Limit Exceeded"),
            ("CTE", "Compile Time Error"),
            ("RE", "Runtime Error"),
            ("MLE", "Memory Limit Exceeded"),
        ),
    )  # four type of submission status(WA, PASS, TLE, CTE)
    language = models.CharField(
        max_length=10, null=True, choices=(("c", "C"), ("c++", "C++"), ("python", "Python"))
    )
    class Meta:
        ordering = ['time']
def get_question_path(state):
    return "Question_Data/{0}".format(state)


class testcase(models.Model):
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    tc_input = models.FileField(null=True, upload_to=get_question_path("Input"))
    tc_output = models.FileField(null=True, upload_to=get_question_path("Output"))


class SetTime(models.Model):
    start_time = models.DateTimeField(auto_now_add=False)
    final_time = models.DateTimeField(auto_now_add=False)


class Question_Status(models.Model):
    q_id = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    p_id = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    penalty=models.IntegerField(null=True,default=0)
    score= models.IntegerField(null=True,default=0)
    status = models.CharField(
        max_length=20,
        null=True,
        choices=(
            ('NA',"Not Attempted"),
            ("WA", "Wrong Answer"),
            ("AC", "Accepted"),
            ("TLE", "Time Limit Exceeded"),
            ("CTE", "Compile Time Error"),
            ("RE", "Runtime Error"),
            ("MLE", "Memory Limit Exceeded")),default="Not Attempted")

class Container(models.Model):
    name=models.CharField(max_length=1003, null=True)
    active=models.BooleanField(null=True,default=False)
    status =models.BooleanField(null=True,default=False)
