# views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm
import jwt
from django.conf import settings
from datetime import datetime, timedelta

class LoginView(View):
    template_name = 'authentication/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                # Создаем JWT токен
                refresh = RefreshToken.for_user(user)
                request.session['jwt_token'] = str(refresh.access_token)
                messages.success(request, 'Successfully logged in!')
                return redirect('authentication:profile')
            else:
                messages.error(request, 'Invalid email or password')
        
        return render(request, self.template_name, {'form': form})

class RegisterView(View):
    template_name = 'authentication/register.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('authentication:profile')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Создаем JWT токен
            refresh = RefreshToken.for_user(user)
            request.session['jwt_token'] = str(refresh.access_token)
            messages.success(request, 'Registration successful!')
            return redirect('authentication:profile')
        return render(request, self.template_name, {'form': form})

class ProfileView(LoginRequiredMixin, View):
    template_name = 'authentication/profile.html'
    login_url = 'authentication:login'
    
    def get(self, request):
        return render(request, self.template_name, {'user': request.user})

def logout_view(request):
    logout(request)
    # Удаляем JWT токен из сессии
    if 'jwt_token' in request.session:
        del request.session['jwt_token']
    messages.success(request, 'Successfully logged out!')
    return redirect('authentication:login')