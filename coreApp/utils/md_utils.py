import os
import requests
import markdown

def get_repo(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def convert_markdown_to_html(markdown_content):
    return markdown.markdown(markdown_content)

def get_markdown_content_from_repo(url):
    markdown_content = get_repo(url)
    html_content = convert_markdown_to_html(markdown_content)

    return html_content