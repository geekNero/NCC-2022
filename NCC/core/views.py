from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from .models import Player,Question, Question_Status
from .serializers import *
from rest_framework.decorators import api_view
from django.db.models import Q
signals = {
    1: "CTE",
    2: "CTE",
    127: "CTE",
    132: "RE",
    133: "RE",
    134: "RE",
    136: "RE",
    137: "TLE",
    138: "MLE",
    139: "RE",
    158: "TLE",
    152: "TLE",
    159: "MLE",
    153: "MLE",
}


# @api_view(['GET', 'POST'])
# def Dashboard(request):
#     User=Player.objects.get(user=request.user.id)
#     ques = Question.objects.filter(Q(junior=User.junior) | Q(junior=None))    
#     status_list=[]
#     for i in ques:
#         status_list.append(Question_StatusSerializer(Question_Status.objects.get_or_create(q_id=i,p_id=User)).data)
#     serializer= QuestionSerilaizer(ques,many=True)
#     print(serializer)
#     return Response({'questions':serializer.data,'status':status_list})



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
