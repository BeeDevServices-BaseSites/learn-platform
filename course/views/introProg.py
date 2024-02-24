from django.shortcuts import render, redirect
from django.contrib import messages
from course.models import *
import markdown
from course.md_utils import *


# title = {
#     'title': '',
#     'header': 'BeeDev Services',
# }

def intro_prog_ch01_pg01(request):
    md = markdown.Markdown(extensions=["fenced_code"])
    markdown_content = MarkdownContent.objects.first()
    markdown_content.content = md.convert(markdown_content.content)
    title = {
        'title': 'MarkDown Test',
        'header': 'MarkDown Test',
    }
    context = {
        'title': title,
        "markdown_content": markdown_content
        }
    return render(request, "intro_prog_ch01_pg01.html", context)

def intro_prog_ch01_pg02(request):
    # md = markdown.Markdown(extensions=["fenced_code"])
    # markdown_content = MarkdownContent.objects.first()
    # markdown_content.content = md.convert(markdown_content.content)
    file_url = 'https://raw.githubusercontent.com/BeeDevServices-BaseSites/test-course/main/programmingIntro/page02.md'
    html_content = get_markdown_content_from_repo(file_url)
    title = {
        'title': 'MarkDown Test',
        'header': 'MarkDown Test',
    }
    markdown_content = {
        'content': html_content, 
        'file_name': file_url
    }
    context = {
        'title': title,
        "markdown_content": markdown_content,
        }
    return render(request, "intro_prog_ch01_pg01.html", context)

