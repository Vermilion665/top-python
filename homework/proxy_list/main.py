import requests
from bs4 import BeautifulSoup
import fake_useragent

# 'https://spys.one'


class Html:
    def __init__(self, url):
        self.ua = fake_useragent.UserAgent()
        self.url = url
        self.headers = {'User-Agent': self.ua.random}

    def html(self):
        return requests.get(self.url, headers=self.headers).text


class Soup(Html):
    def soup(self):
        return BeautifulSoup(self.html(), 'lxml')


class Table(Soup):
    def table(self):
        return self.soup().find('tr', class_="spy1x").find_parent().find_all('tr')[1:-1]


class Keys(Table):
    def __init__(self, url):
        super().__init__(url)
        self.__table = self.table()

    def keys_list(self):
        return [i.text for i in self.__table[0]]


class Values(Table):
    def __init__(self, url):
        super().__init__(url)
        self.__table = self.table()

    def values_list(self):
        return [[i.text for i in link.find_all('td')] for link in self.__table[1:]]


class DictProxy(Keys, Values):
    def __init__(self, url):
        super().__init__(url)
        self.keys_list = self.keys_list()
        self.values_list = self.values_list()

    def dict_proxy_list(self):
        return [{self.keys_list[j]: self.values_list[i][j] for j in range(len(self.keys_list))} for i in
                range(len(self.values_list))]


with open('proxy-list.txt', 'w') as fb:
    for i in DictProxy('https://spys.one').dict_proxy_list():
        fb.write(str(i) + '\n')
