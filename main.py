from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.timesjobs.com/job-search?cboPresFuncArea=35&refreshed=true')
soup=BeautifulSoup(html_text,'lxml')
jobs = soup.find_all('li',class_="p-4 md:p-6 bg-white rounded-xl mb-4 shadow-sm relative srp-card" )

# # as the youtube guy said i have done the same steps here need to find a solution for the errrs in the terminal