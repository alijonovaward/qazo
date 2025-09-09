from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from namoz.models import Namoz

# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Parollar mos kelmadi!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username mavjud")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        from namoz.models import Namoz
        Namoz.objects.create(
            user=user,
            bomdod=0,
            peshin=0,
            asr=0,
            shom=0,
            xufton=0,
            vitr=0
        )

        messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
        return redirect('setup_qazo')

    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            Namoz.objects.get_or_create(
                user=user,
                defaults={
                    "bomdod": 0,
                    "peshin": 0,
                    "asr": 0,
                    "shom": 0,
                    "xufton": 0,
                    "vitr": 0,
                }
            )
            return redirect('home')
        else:
            messages.error(request, "Username yoki parol xato!")
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

