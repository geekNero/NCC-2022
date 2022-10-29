from .models import *
from .serializers import *
from .time import time_left
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .permission import TimePermit
from django.shortcuts import get_object_or_404
from .functionality import custom,run_code,run_updates
from rest_framework.decorators import api_view
from .pagination import *
from rest_framework.pagination import PageNumberPagination
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
    pagination_class=SubmissionPagination
    page_size = 5
    def get_queryset(self):
        return self.queryset.filter(p_id=self.request.user)
    def retrieve(self, request, pk=None):
        paginator = PageNumberPagination()
        paginator.page_size = self.page_size
        submission=self.get_queryset().filter(q_id=Question.objects.get(id=pk))
        result_page = paginator.paginate_queryset(submission, request)
        serializer= self.get_serializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
        
        
class AllQuestionStatus(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Question_Status.objects.all()
    serializer_class=Question_StatusSerializer
    def get_queryset(self):
        return self.queryset.filter(p_id=self.request.user)
    def retrieve(self, request, pk=None):
        questionStatus=get_object_or_404(self.get_queryset(),q_id=Question.objects.get(id=pk))
        serializer= self.get_serializer(questionStatus)
        return Response(serializer.data)

class UserDetails(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Player.objects.all()
    serializer_class=PlayerSerializer
    def fetch(self,request):
        try:
            player=get_object_or_404(self.queryset,id=request.user.id)
            serializer= self.get_serializer(player)
            return Response(serializer.data)
        except:
            return Response(["Failed"])

class Leaderboard(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Player.objects.all().order_by("-total_score")    
    page_size = 10
    paginator = PageNumberPagination()
    def userRank(self,request):
        try:
            myrank={}
            rank=1
            for player in self.queryset:
                if(player.id==request.user.id):
                    myrank["rank"]=rank
                    for que in Question.objects.all():
                        status,created=Question_Status.objects.get_or_create(p_id=player,q_id=que)
                        myrank[status.q_id.pk]=status.status
                    break
                rank+=1
            return Response(myrank)
        except:
            return Response(["Failed"])
    def allRanks(self,request):
        try:
            paginator = PageNumberPagination()
            paginator.page_size = self.page_size
            ret={}
            rank=[]
            for player in self.queryset:
                ret['name']={player.username}
                ret['total_score']=player.total_score
                for que in Question.objects.all():
                    status,created=Question_Status.objects.get_or_create(p_id=player,q_id=que)
                    ret[status.q_id.id]=status.score
                rank.append(ret)
            result_page = paginator.paginate_queryset(rank, request)
            return paginator.get_paginated_response(result_page)
        except:
            return Response(["Failed"])
        
class Submit(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    def submission(self,request,pk):
        if(request.method=="POST"):
            try:
                code=request.POST["code"]
                language=request.POST["language"]
                test_ops,error=run_code(code,language,pk)
                test_ops,error=run_updates(pk,test_ops,error,request.user,code,language)
                return Response({"cases":test_ops,"error":error})
            except:
                return Response(["Failed"])
    def customSubmission(self,request):
        try:
            if(request.method=="POST"):
                code=request.POST["code"]
                inp=request.POST["input"]
                language=request.POST["language"]
                output,error=custom(code,language,inp)
                return Response({"output":output,"error":error})
        except:
            return Response(["Failed"])

#returns a dictionary containing hours, mins, and seconds of current time since start of the contest
@api_view(['GET'])
def Time(request):
    return Response(time_left())
