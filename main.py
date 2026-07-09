from bs4 import BeautifulSoup

with open('website.html', 'r') as html_file:

    # read() shows the exact code
    content = html_file.read() # print(content)

    #by using beatifulsoup we are apply lxml format to the content  
    soup=BeautifulSoup(content, 'lxml') # print(soup)
    course_cards=soup.find_all('div', class_="card mb-3")
    for course in course_cards:
       course_name=course.h3.text
       course_price=course.a.text.split()[-1]

       print(f'{course_name} costs {course_price}')