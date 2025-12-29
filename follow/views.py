from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def friends(request):
    users = User.objects.all()

    context = {'users':users}
    return render(request, 'follow/userlist.html', context)

def get_followers(request):
    user = request.user
    followers_users = User.objects.filter(
        following__following=user,
        following__status='accepted'
    )
    return render(request, 'follow/userlist.html', {'users':followers_users})