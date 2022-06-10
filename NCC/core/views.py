from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from .models import UserAccount,Question, Question_Status
from .serializers import UserSerializer, Question_StatusSerializer, QuestionSerilaizer
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
#     User=UserAccount.objects.get(user=request.user.id)
#     ques = Question.objects.filter(Q(junior=User.junior) | Q(junior=None))    
#     status_list=[]
#     for i in ques:
#         status_list.append(Question_StatusSerializer(Question_Status.objects.get_or_create(q_id=i,p_id=User)).data)
#     serializer= QuestionSerilaizer(ques,many=True)
#     print(serializer)
#     return Response({'questions':serializer.data,'status':status_list})



