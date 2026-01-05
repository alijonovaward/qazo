from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Permission

# Create your views here.
def friends(request):
    users = User.objects.all()

    context = {'users':users, 'followers':False}
    return render(request, 'follow/userlist.html', context)

def get_followers(request):
    permissions = Permission.objects.filter(receiver=request.user)
    users = [p.sender for p in permissions]

    context = {'users':users, 'followers':True}

    return render(request, 'follow/userlist.html', context)