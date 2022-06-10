from django.urls import path, include
from django.views.generic import TemplateView # for reaact side.

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]