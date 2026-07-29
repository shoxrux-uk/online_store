from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from shop.models import Order

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('product_list')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Попытка входа: {username} / {password}") 
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Вы вошли в систему!')
            return redirect('product_list')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('/')

@login_required
def profile(request):
    orders = Order.objects.filter(is_completed=True).order_by('-created_at')
    return render(request, 'users/profile.html', {'orders': orders})