from bs4 import BeautifulSoup

with open('website.html', 'r') as html_file:

    # read() shows the exact code
    content = html_file.read()

    #by using beatifulsoup we are apply lxml format to the content  
    soup=BeautifulSoup(content, 'lxml')

    # find() searches and gives the first tag
    # find_all() searches and gives all the tags in a
    # #tags=soup.find('h2') here we can only insert the tag names to get some output
    tags=soup.find_all('h2')
    print(tags)