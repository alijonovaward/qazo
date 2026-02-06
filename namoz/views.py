from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NamozForm
from .models import Namoz, NamozAction
from django.utils import timezone
import pytz

# Create your views here.
@login_required
def home(request):
    namoz, created = Namoz.objects.get_or_create(
        user=request.user,
        defaults={'bomdod': 0, 'peshin': 0, 'asr': 0, 'shom': 0, 'xufton': 0, 'vitr':0}
    )

    # Faqat shu userning oxirgi 20 ta amalini olish
    from .models import NamozAction
    actions = NamozAction.objects.filter(user=request.user).order_by('-created_at')[:20]

    # Namoz obyektini dictionaryga aylantiramiz
    qazo_dict = {
        "bomdod": namoz.bomdod,
        "peshin": namoz.peshin,
        "asr": namoz.asr,
        "shom": namoz.shom,
        "xufton": namoz.xufton,
        "vitr": namoz.vitr,
    }

    return render(request, "namoz/home.html", {"qazo": qazo_dict, "actions": actions})

@login_required
def setup_qazo(request):
    namoz, created = Namoz.objects.get_or_create(
        user=request.user,  # foydalanuvchiga bog'lash
        defaults={
            'bomdod': 0,
            'peshin': 0,
            'asr': 0,
            'shom': 0,
            'xufton': 0,
        }
    )

    if request.method == "POST":
        form = NamozForm(request.POST, instance = namoz)
        if form.is_valid():
            new_namoz = form.save(commit = False)
            new_namoz.user = request.user
            new_namoz.save()
            return redirect('home')
    else:
        form = NamozForm(instance = namoz)

    return render(request, 'namoz/setup_qazo.html', {'form': form})

@login_required
def update_qazo(request):
    if request.method == 'POST':
        prayer = request.POST.get('prayer')
        action = request.POST.get('action')

        if prayer not in ["bomdod", "peshin", "asr", "shom", "xufton", "vitr"]:
            return JsonResponse({"success": False, "error": "Invalid prayer name"})

        namoz = Namoz.objects.get(user=request.user)
        current_val = getattr(namoz, prayer)
        old_val = current_val  # <-- qo‘shdik

        if action == "+":
            setattr(namoz, prayer, current_val + 1)
        elif action == "-" and current_val > 0:
            setattr(namoz, prayer, current_val - 1)

        namoz.save()
        new_val = getattr(namoz, prayer)

        TASHKENT_TZ = pytz.timezone('Asia/Tashkent')

        # Tarixga yozamiz
        from .models import NamozAction
        NamozAction.objects.create(
            user=request.user,
            prayer=prayer,
            action=action,
            old_value=old_val,
            new_value=new_val,
        )

        # Faqat 20 ta oxirgisini qoldiramiz
        actions = NamozAction.objects.filter(user=request.user).order_by('-created_at')[:20]

        # JSON qaytaramiz (faqat bitta qiymat emas, balki butun tarix ham)
        actions_data = [
            {
                "prayer": a.prayer,
                "action": a.action,
                "old_value": a.old_value,
                "new_value": a.new_value,
                "created_at": a.created_at.astimezone(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            }
            for a in actions
        ]

        return JsonResponse({
            "success": True,
            "new_value": new_val,
            "actions": actions_data
        })

    return JsonResponse({"success": False})

@login_required
def namoz_total_chart(request):
    TASHKENT_TZ = pytz.timezone('Asia/Tashkent')

    # Faqat o‘sha userning actionlarini vaqt bo‘yicha oling
    actions = NamozAction.objects.filter(user=request.user).order_by('created_at')
    namoz = Namoz.objects.get(user=request.user)

    total = namoz.bomdod + namoz.peshin + namoz.asr + namoz.shom + namoz.xufton + namoz.vitr
    chart_data = []

    for a in actions:
        total += a.new_value - a.old_value

        chart_data.append({
            "time": a.created_at.astimezone(TASHKENT_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "total": total
        })

    return JsonResponse(chart_data, safe=False)