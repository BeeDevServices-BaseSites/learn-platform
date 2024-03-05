from django.shortcuts import render, redirect
from django.contrib import messages
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
    context = {
        'title': title,
    }
    return render(request, 'index.html', context)

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            if userLogin.level == 0:
                messages.error(request, 'Welcome please create a new password!')
                return redirect('/set-password/')
            messages.error(request, f'Welcome back {userLogin.fullName()}')
            return redirect('/dashboard/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/')
    messages.error(request, "That Email is not in our system, please reach out to support")
    return redirect('/')

def register(request):
    if request.method == 'GET':
        return redirect('/queen/bees/admin-register/')
    theCode = request.POST['reg_code']
    if theCode != REG_CODE:
        messages.error(request, 'Invalid Registration Code')
        return redirect('/queen/bees/admin-register/')
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect('/queen/bees/admin-register/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    if newUser.id == 1:
        toUpdate = User.objects.get(id=request.session['user_id'])
        toUpdate.level=24
        toUpdate.save()
    messages.error(request, f'Welcome {newUser.firstName}')
    return redirect('/dashboard')

def dashboard(request):
    title = {
        'title': 'Dashboard',
        'header': 'TechByte Learning',
    }
    if 'user_id' not in request.session:
        user = False
    context = {
        'title': title,
    }
    return render(request, 'index.html', context)

def admin_register(request):
    title = {
        'title': 'Queen Bees Admin Register',
        'header': 'TechByte Learning',
    }
    if 'user_id' not in request.session:
        user = False
    context = {
        'title': title,
    }
    return render(request, 'registration.html', context)