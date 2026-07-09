from bs4 import BeautifulSoup

with open('website.html', 'r') as html_file:
    content = html_file.read()
    print(content)