from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            try:
                # Validate the password to check its strength
                validate_password(password, user=User)
            except ValidationError as e:
                # If the password is weak, display an error message
                messages.error(request, "Password is too weak. " + str(e))
                return redirect('signup')
            
            # If the password is strong, proceed with user creation
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Account created successfully")
            return redirect('login')
        else:
            # If the form is invalid, display an error message
            messages.error(request, "Improve strength of password")
            return redirect('signup')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'signup.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('user_view',username=username)
         
        messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
        
    context = {'form': form}
    return render(request, 'login.html', context)
    


def user_view(request,username):

    return render(request, 'user_view.html', {'username':username})

