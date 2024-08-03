from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from accounts.forms import RegisterUserForm, ChangePassUser


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Username or Password is incorrect')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You were logged out')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You were registered successfully')
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/register_user.html',
           {'form': form}, )

def change_password(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ChangePassUser(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = ChangePassUser(user = request.user)
    context= {'form':form}
    return render(request,'authenticate/changepass.html',context)
