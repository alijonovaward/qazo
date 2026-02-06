from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends, name='userlist'),
    path('followers/', views.get_followers, name='followers'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('chart/<int:user_id>/', views.chart_page, name='chart_page'),
    path('get_chart_data/<int:user_id>', views.namoz_total_chart_follow, name='namoz_total_chart_follow'),
]