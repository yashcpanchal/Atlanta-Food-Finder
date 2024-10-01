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
        
        if not security_question or not security_answer:
            return HttpResponse('Please provide a security question and answer.')

        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Create or get the user's profile with security question and answer
            profile, created = Profile.objects.get_or_create(user=user)
            print('x')
            profile.security_question = security_question
            print('y')
            profile.security_answer = security_answer
            print('z')
            profile.save()  # Save the profile
            print('save')

            # print(f"Created Profile: {profile}, Security Question: {profile.security_question}, Security Answer: {profile.security_answer}")
            
            # login(request, user)  # Log the user in automatically after registration
            return HttpResponse('Registration successful!')

        except IntegrityError as e:
            return HttpResponse('Profile for this user already exists.')
        except Exception as e:
            print(f"Error creating user: {e}")
            return HttpResponse('An error occurred during registration. Please try again.')
    
    return render(request, 'register.html')

def request_username_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        # Check if the user exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            request.session['reset_username'] = username  # Store the username in session
            return redirect('reset_password')  # Redirect to the security question form
        else:
            return HttpResponse('Username does not exist.')
    return render(request, 'request_username.html')

def reset_password_view(request):
    username = request.session.get('reset_username', None)
    if not username:
        return HttpResponse('No username provided.')

    user = User.objects.get(username=username)

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        return HttpResponse('No profile found for this user.')
    
    print(f"Created Profile: {profile}, Security Question: {profile.security_question}, Security Answer: {profile.security_answer}")

    if request.method == 'POST':
        answer = request.POST['security_answer'].strip().lower()
        if answer == profile.security_answer.strip().lower():
            # Correct answer, allow password reset
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return HttpResponse('Password reset successful!')
            else:
                return HttpResponse('Passwords do not match.')
        else:
            return HttpResponse('Security answer is incorrect.')
    
    return render(request, 'reset_password_question.html', {'security_question': profile.security_question})
