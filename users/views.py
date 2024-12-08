from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # log in the user
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('solutions:solution-list')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'users/techlog_login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e)
            return render(request, 'users/techlog_signup.html')

        # Password validating
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'users/techlog_signup.html')
        
        # Check if username/email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'users/techlog_signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return render(request, 'users/techlog_signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)
        return redirect('solutions:solution-list')

    return render(request, 'users/techlog_signup.html')

def logout_view(request):
    logout(request)
    return redirect('solutions:solution-list')

def user_profile(request, username):
    # Pobierz użytkownika na podstawie nazwy użytkownika lub zwróć błąd 404
    user = get_object_or_404(User, username=username)
    
    # Renderuj stronę profilu użytkownika
    return render(request, 'users/user_profile.html', {'profile_user': user})