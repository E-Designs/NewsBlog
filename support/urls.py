import imp
from django.urls import path
from .import views

urlpatterns = [
    path('support', views.support, name='support'),
    path('support/submitted', views.support_submitted, name='support_submitted'),
]
