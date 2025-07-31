from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import sys

def register(request):
    print("View called", file=sys.stderr)
    if request.method == "POST":
        print("POST received", file=sys.stderr)
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(f"Data: username={username}, email={email}, password={password}", file=sys.stderr)
            if not all([username, email, password]):
                print("Missing fields", file=sys.stderr)
                return render(request, 'users/register.html', {'error': 'All fields are required'})
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                print("Username exists, redirecting to login", file=sys.stderr)
                return redirect('/users/login/')  # Redirect existing users to login
            user = User.objects.create_user(username=username, email=email, password=password)
            print(f"User created: {user}, redirecting to login", file=sys.stderr)
            return redirect('/users/login/')  # Redirect new users to login
        except Exception as e:
            print(f"Exception: {e}", file=sys.stderr)
            return render(request, 'users/register.html', {'error': f'Error: {str(e)}'})
    print("Rendering register page", file=sys.stderr)
    return render(request, 'users/register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("User authenticated in login, redirecting to /smart_pdf/", file=sys.stderr)
            return redirect('/smart_pdf/')  # Direct path to upload page
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')