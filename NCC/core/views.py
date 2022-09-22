from rest_framework import mixins
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .permission import TimePermit
from django.shortcuts import render, get_object_or_404
from .functionality import run_code,run_updates
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

class AllQuestion(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Question.objects.all()
    serializer_class= QuestionSerilaizer
    # def list(self, request):
    #     serializer = self.get_serializer(self.get_queryset(), many=True)
    #     return Response(serializer.data)
    # def retrieve(self, request, pk = None):
    #     question=get_object_or_404(self.queryset, pk = pk)
    #     serializer = self.get_serializer(question)
    #     return Response(serializer.data)
    # print(time_left())
class Submissions(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Submission.objects.all()
    serializer_class=SubmissionSerializer
    def get_queryset(self):
        return self.queryset.filter(p_id=Player.objects.get(id=self.request.user.id))
    def retrieve(self, request, pk=None):
        submission=get_object_or_404(self.get_queryset(request),q_id=Question.objects.get(id=pk))
        serializer= self.get_serializer(submission)
        return Response(serializer.data)
        
class AllQuestionStatus(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Question_Status.objects.all()
    serializer_class=Question_StatusSerializer
    def get_queryset(self):
        return self.queryset.filter(p_id=Player.objects.get(id=self.request.user.id))
    def retrieve(self, request, pk=None):
        questionStatus=get_object_or_404(self.get_queryset(request),q_id=Question.objects.get(id=pk))
        serializer= self.get_serializer(questionStatus)
        return Response(serializer.data)

class UserDetails(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Player.objects.all()
    serializer_class=PlayerSerializer
    def fetch(self,request):
        player=get_object_or_404(self.queryset,id=request.user.id)
        serializer= self.get_serializer(player)
        return Response(serializer.data)

class Leaderboard(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Player.objects.all().order_by("-total_score")    
    def userRank(self,request):
        myrank=-1
        rank=1
        for i in self.queryset:
            if(i.id==request.user.id):
                myrank=rank
                break
            rank+=1
        return Response([rank])

    def allRanks(self,request):
        ret=[]
        for i in self.queryset:
            lst=[i.username]
            each_score=[]
            for j in Question.objects.all():
                status,created=Question_Status.objects.get_or_create(p_id=i,q_id=j)
                each_score.append(status.score)
            lst.append(each_score)
            lst.append(i.total_score)
            ret.append(lst)
        return Response(ret)
class Submit(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    def submission(self,request,pk):
        if(request.method=="POST"):
            code=request.POST["code"]
            language=request.POST["language"]
            test_ops,error=run_code(code,language,pk)
            test_ops,error=run_updates(pk,test_ops,error,request.user,code,language)
            return Response({"cases":test_ops,"error":error})
        return Response(["Failed"])