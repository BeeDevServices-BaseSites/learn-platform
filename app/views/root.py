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
    context = {
        'title': title,
    }
    return render(request, 'index.html', context)