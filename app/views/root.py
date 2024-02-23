from django.shortcuts import render, redirect
from django.contrib import messages


# title = {
#     'title': '',
#     'header': 'BeeDev Services',
# }

def index(request):
    title = {
    'title': 'TechByte',
    'header': 'BeeDev Services',
}
    context = {
        'title': title
    }
    return render(request, 'template.html', context)