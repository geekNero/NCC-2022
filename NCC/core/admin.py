from django.contrib import admin
from django.db import models
from .models import *

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["username", "total_score"]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "score",
        "title",
        "body",
        "correct_submissions",
        "total_submissions",
    ]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["p_id", "q_id", "time", "code", "language", "status"]


@admin.register(testcase)
class TestcaseAdmin(admin.ModelAdmin):
    list_display = ["q_id"]


@admin.register(SetTime)
class SetTimeAdmin(admin.ModelAdmin):
    list_display = ["start_time", "final_time"]

@admin.register(Question_Status)
class Question_StatusAdmin(admin.ModelAdmin):
    list_display = ['q_id', 'p_id','penalty', 'score', 'status']

@admin.register(Container)
class Container_Statusadmin(admin.ModelAdmin):
    list_display = ['name','cid','status']