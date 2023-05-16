import requests
from bs4 import BeautifulSoup
import fake_useragent
import re

url = 'https://ru.wikipedia.org/wiki/Silicon_Valley_Bank'
ua = fake_useragent.UserAgent()
headers = {'User-Agent': ua.random}
resp = requests.get(url, headers=headers).text
soup = BeautifulSoup(resp, 'lxml')
links = soup.find_all('a')
wiki_url = soup.find('link', rel='canonical').get('href')

with open('wiki_links.txt', 'w', encoding='utf-8') as fl:
    fl.write(f"{soup.find('title').text} - {wiki_url}" + '\n')
    for i in links:
        if (i.text or i.get('title')) is None:
            del i
        else:
            link = i.get('href')
            if re.match('[^htps]', link):
                link = f"https://ru.wikipedia.org/wiki{link}"
                fl.write(f"{i.text or i.get('title')} - {link}" + '\n')
            else:
                fl.write(f"{i.text or i.get('title')} - {link}" + '\n')
