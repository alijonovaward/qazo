import pytz
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Permission
from django.contrib.auth.models import User

from namoz.models import Namoz, NamozAction

# Create your views here.
@login_required
def friends(request):
    users = User.objects.exclude(id=request.user.id)  # o'zingizni chiqarib tashlaymiz
    # request.user yuborgan barcha permissionlarni olish
    permissions = Permission.objects.filter(sender=request.user)
    context = {
        'users': users,
        'permissions': permissions,
        'followers': False
    }
    return render(request, 'follow/userlist.html', context)

def get_followers(request):
    permissions = Permission.objects.filter(receiver=request.user)
    users = [p.sender for p in permissions]

    context = {'users':users, 'followers':True}

    return render(request, 'follow/userlist.html', context)

@login_required
def follow_user(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    Permission.objects.update_or_create(
        sender=request.user,
        receiver=receiver,
        defaults={'status':'accepted'}  # yoki 'pending' qilishingiz mumkin
    )
    return redirect('userlist')

@login_required
def unfollow_user(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    Permission.objects.filter(sender=request.user, receiver=receiver, status='accepted').delete()
    return redirect('userlist')

@login_required
def namoz_total_chart_follow(request, user_id):
    user = get_object_or_404(User, id=user_id)
    TASHKENT_TZ = pytz.timezone('Asia/Tashkent')

    # Faqat o‘sha userning actionlarini vaqt bo‘yicha oling
    actions = NamozAction.objects.filter(user=user).order_by('created_at')
    namoz = Namoz.objects.get(user=user)

    total = namoz.bomdod + namoz.peshin + namoz.asr + namoz.shom + namoz.xufton + namoz.vitr
    chart_data = []

    for a in actions:
        total += a.new_value - a.old_value

        chart_data.append({
            "time": a.created_at.astimezone(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "total": total
        })

    return JsonResponse(chart_data, safe=False)

@login_required
def chart_page(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "follow/chart.html", {"chart_user": user})
