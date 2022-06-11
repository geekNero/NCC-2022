from .models import *
from rest_framework import serializers

class PlayerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=Player
        fields="__all__"

    def create(self,data):
        user=Player.objects.create(
            username = data['username'],
            email = data['email'],
            junior=data['junior'],
            total_score=0
        )
        user.set_password(data['password'])
        user.save()
        return user
class QuestionSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    q_id = QuestionSerilaizer(read_only=True, many=True) # just to pass data along with json object.
    p_id = PlayerSerializer(read_only=True, many=True)
    class Meta:
        model = Submission
        fields = "__all__"


class TestcaseSerializer(serializers.ModelSerializer):
    q_id = QuestionSerilaizer(read_only=True, many=True) 
    class Meta:
        model = testcase
        fields = "__all__"
    
class SetTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetTime
        fields = '__all__'

class Question_StatusSerializer(serializers.ModelSerializer):
    q_id = QuestionSerilaizer(read_only=True, many=True) # just to pass data along with json object.
    p_id = PlayerSerializer(read_only=True, many=True)
    class Meta:
        model = Question_Status
        fields = '__all__'

