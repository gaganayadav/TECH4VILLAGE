from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser


def get_started(request):
    return render(request, 'index.html') 

def admin_check(user):
    """Check if user is authenticated and has admin privileges"""
    return user.is_authenticated and (user.is_admin() or user.is_superuser)

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')

@login_required
@user_passes_test(admin_check, login_url='dashboard')
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request=request)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm(request=request)
    
    context = {
        'form': form,
        'is_admin': request.user.is_admin() or request.user.is_superuser
    }
    return render(request, 'accounts/register.html', context)