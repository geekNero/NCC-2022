from .models import UserAccount, Question, Submission, testcase, Question_Status, SetTime
from rest_framework import serializers


from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model() #since custom user model

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = '__all__'

#     # def create(self,data):
#     #     user = User.objects.create(
#     #         username = data['username'],
#     #         email = data['email'],
#     #         total_score=0,
#     #     )
#     #     user.set_password(data['password'])
#     #     user.save()
#     #     return user

class QuestionSerilaizer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    q_id = QuestionSerilaizer(read_only=True, many=True) # just to pass data along with json object.
    p_id = UserCreateSerializer(read_only=True, many=True)
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
    p_id = UserCreateSerializer(read_only=True, many=True)
    class Meta:
        model = Question_Status
        fields = '__all__'

