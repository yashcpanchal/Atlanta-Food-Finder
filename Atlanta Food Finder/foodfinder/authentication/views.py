from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Profile
from django.db import IntegrityError


def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Logged in successfully!')
        else:
            return HttpResponse('Invalid credentials.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/auth/login/')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        security_question = request.POST['security_question']
        security_answer = request.POST['security_answer']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse('Username already exists. Please choose another one.')

        # Check if the passwords match
        if password != confirm_password:
            return HttpResponse('Passwords do not match.')

        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            
            # Check if the user already has a profile (just a precaution)
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user, security_question=security_question, security_answer=security_answer)

            login(request, user)  # Log the user in automatically after registration
            return HttpResponse('Registration successful!')

        except IntegrityError as e:
            return HttpResponse('Profile for this user already exists.')
        except Exception as e:
            print(f"Error creating user: {e}")
            return HttpResponse('An error occurred during registration. Please try again.')
    
    return render(request, 'register.html')

def reset_password_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.filter(username=username).first()

        if user:
            profile = user.profile
            if request.POST.get('security_answer'):
                security_answer = request.POST['security_answer']
                if profile.security_answer == security_answer:
                    # Allow the user to reset the password
                    new_password = request.POST['new_password']
                    confirm_password = request.POST['confirm_password']
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        user.save()
                        return HttpResponse('Password reset successfully!')
                    else:
                        return HttpResponse('Passwords do not match.')
                else:
                    return HttpResponse('Incorrect security answer.')
            else:
                # Render the form to ask the security question
                return render(request, 'reset_password_question.html', {'question': profile.security_question})
        else:
            return HttpResponse('Username not found.')

    return render(request, 'reset_password.html')
# Create your views here.
