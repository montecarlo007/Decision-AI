from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import User
import datetime

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
            
        if User.objects(email=email).first():
            messages.error(request, 'Email already registered')
            return redirect('register')
            
        user = User(email=email, role='user')
        user.set_password(password)
        user.save()
        
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.GET.get('next')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                user.last_login = datetime.datetime.utcnow()
                user.save()
                request.session['user_id'] = str(user.id)
                
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                
                if user.is_staff:
                    return redirect('admin_dashboard')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            
        return redirect('login')

def logout_view(request):
    request.session.flush()
    return redirect('login')
