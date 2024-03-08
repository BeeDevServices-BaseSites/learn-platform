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

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            if userLogin.is_default_pass == 1:
                messages.error(request, 'Welcome please create a new password!')
                return redirect('/set-password/')
            else:
                toUpdate = User.objects.get(id=request.session['user_id'])
                toUpdate.logged_on = timezone.now()
                toUpdate.save()
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
        toUpdate.is_default_pass=0
        toUpdate.profile.is_staff=1
        toUpdate.save()
    messages.error(request, f'Welcome {newUser.first_name}')
    return redirect('/dashboard')

