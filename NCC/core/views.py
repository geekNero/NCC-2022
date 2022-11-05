from .models import *
from .serializers import *
from .time import current_time
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .permission import TimePermit
from django.shortcuts import get_object_or_404
from .functionality import custom,run_code,run_updates,run_container
from rest_framework.decorators import api_view
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
        return self.queryset.filter(p_id=self.request.user)
    def retrieve(self, request, pk=None):
        submission=self.get_queryset().filter(q_id=Question.objects.get(id=pk))
        serializer= self.get_serializer(submission,many=True)
        return Response(serializer.data)
    def buffer(self,request,pk=None):
        try:
            submission=self.get_queryset().filter(q_id=Question.objects.get(id=pk)).order_by("-time")
            serializer= self.get_serializer(submission[0])
            return Response(serializer.data)
        except:
            return Response(["Failed"])
        
class AllQuestionStatus(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    queryset=Question_Status.objects.all()
    serializer_class=Question_StatusSerializer
    def create_status(self):
        for que in Question.objects.all():
            Question_Status.objects.get_or_create(p_id=self.request.user,q_id=que)
    def get_queryset(self):
        self.create_status()
        return self.queryset.filter(p_id=self.request.user)
    def retrieve(self, request, pk=None):
        questionStatus=get_object_or_404(self.get_queryset(),q_id=Question.objects.get(id=pk))
        serializer= self.get_serializer(questionStatus)
        return Response(serializer.data)

class UserDetails(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated)
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
    permission_classes=(IsAuthenticated)
    queryset=Player.objects.all().order_by("-total_score")    
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
            ret={}
            for player in self.queryset:
                ret[player.username]={}
                ret[player.username]['total_score']=player.total_score
                for que in Question.objects.all():
                    status,created=Question_Status.objects.get_or_create(p_id=player,q_id=que)
                    ret[player.username][status.q_id.id]=status.score
            return Response(ret)
        except:
            return Response(["Failed"])
        
class Submit(viewsets.ModelViewSet):
    permission_classes=(IsAuthenticated,TimePermit)
    def submission(self,request,pk):
        try:
            if(request.method=="POST"):
                run_container()
                code=request.POST["code"]
                language=request.POST["language"]
                submission_time=current_time()
                test_ops,error=run_code(code,language,pk)
                test_ops,error=run_updates(pk,test_ops,error,request.user,code,language,submission_time)
                return Response({"cases":test_ops,"error":error})
        except:
            return Response(["Failed"])
    def customSubmission(self,request):
        try:
            if(request.method=="POST"):
                run_container()
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
    t=SetTime.objects.get(pk=1)
    return Response({"start_time":t.start_time,"end_time":t.final_time})