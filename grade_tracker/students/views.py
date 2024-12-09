from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentRegistrationForm
from grades.models import Student

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user (using UserCreationForm)
            user = form.save()

            # Create the associated Student instance
            if form['name'] is not None:
                student = Student.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email']
                )
            else:
                    student = Student.objects.create(
                    user=user,
                    name=form.cleaned_data['username'],
                    email=form.cleaned_data['email']
                )
                
            # Log the user in after registration
            login(request, user)
            messages.success(request, "Registration successful! Please log in.")
            return redirect('home')  # Or redirect to another page
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'home') 
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')

