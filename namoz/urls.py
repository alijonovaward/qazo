from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('setup/', views.setup_qazo, name = 'setup_qazo'),
    path('update_qazo/', views.update_qazo, name='update_qazo'),
    path('get_chart/', views.namoz_total_chart, name='namoz_total_chart'),
]