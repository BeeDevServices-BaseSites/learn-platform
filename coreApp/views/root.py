from django.shortcuts import render, redirect
from django.contrib import messages


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

def test(request):
    title = {
        'title': 'Home',
        'header': 'TechByte Learning',
    }
    if 'user_id' not in request.session:
        user = False
    context = {
        'title': title,
    }
    return render(request, 'dashboard.html', context)