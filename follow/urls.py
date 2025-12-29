from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends, name='userlist'),
    path('followers/', views.get_followers, name='followers'),
]