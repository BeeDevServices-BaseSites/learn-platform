from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from coreApp.models import *
import bcrypt
from environ import Env

env = Env()
env.read_env()

REG_CODE = env('REG_CODE')
print(REG_CODE)

# title = {
#     'title': '',
#     'header': 'BeeDev Services',
# }

def index(request):
    title = {
        'title': 'Home',
        'header': 'TechByte Learning',
    }
    if 'user_id' not in request.session:
        user = False
    allUsers = User.objects.all().values()
    if not allUsers:
        return redirect('/queen/bees/admin-register/')
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        return redirect('/dashboard/')
    context = {
        'title': title,
        'user': user,
    }
    return render(request, 'index.html', context)

def dashboard(request):
    title = {
        'title': 'Dashboard',
        'header': 'TechByte Learning',
    }
    if 'user_id' not in request.session:
        user = False
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'title': title,
        'user': user,
    }
    return render(request, 'dashboard.html', context)

def admin_register(request):
    title = {
        'title': 'Queen Bees Admin Register',
        'header': 'TechByte Learning',
    }
    if 'user_id' not in request.session:
        user = False
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'title': title,
        'user': user,
    }
    return render(request, 'registration.html', context)

def logout(request):
    request.session.clear()
    messages.error(request, 'You have been logged out')
    return redirect('/')