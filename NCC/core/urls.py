from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('question', views.AllQuestion.as_view(actions={'get': 'list'}), name = 'question'),
    path('question/<int:pk>', views.AllQuestion.as_view(actions={'get': 'retrieve'}), name = 'retrieve-question'),
    path('status', views.AllQuestionStatus.as_view(actions={'get': 'list'}), name = 'questionStatus'),
    path('status/<int:pk>', views.AllQuestionStatus.as_view(actions={'get': 'retrieve'}), name = 'retrieve-questionStatus'),
    path('user',views.UserDetails.as_view(actions={'get':'fetch'}),name='UserDetails'),
    path('rank',views.Leaderboard.as_view(actions={'get':'userRank'}),name='UserRank'),
    path('allranks',views.Leaderboard.as_view(actions={'get':'allRanks'}),name='AllRanks'),
]