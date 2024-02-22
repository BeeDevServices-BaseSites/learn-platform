from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from app.forms import LoginForm

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
    context = {
        'title': title,
    }
    return render(request, 'index.html', context)


def userLogin(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard upon successful login
            else:
                error_message = "Invalid email or password"
    else:
        form = LoginForm()
        error_message = None
    return render(request, 'login.html', {'form': form, 'error_message': error_message})