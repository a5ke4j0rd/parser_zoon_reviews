import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class HtmlLoader:
    __headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    }

    def __init__(self, url):
        self.url = url

    def load(self):
        response = requests.get(self.url, headers=self.__headers, timeout=5)
        return BeautifulSoup(response.text, 'lxml')

class DataParser(ABC):
    @abstractmethod
    def parse(self, data):
        pass

class StarsParser(DataParser):
    def parse(self, data):
        stars = data.find_all('div', {'data-uitest': 'personal-mark'})
        for star in stars:
            print(star.text)

class AuthorParser(DataParser):
    def parse(self, data):
        authors = data.find_all('span', {'itemscope': '', 'itemtype': 'https://schema.org/Person'})
        for author in authors:
            author_name = author.find('span').text.strip()
            print(author_name)

class ReviewParser(DataParser):
    def parse(self, data):
        reviews = data.find_all('div', {'data-uitest': 'comment-details-text'})
        for review in reviews:
            review_text = review.find('span', class_='js-comment-content').text.strip()
            print(review_text)

class Parser:
    def __init__(self, url):
        self.loader = HtmlLoader(url)
        self.parsers = []

    def add_parser(self, parser: DataParser):
        self.parsers.append(parser)

    def run(self):
        data = self.loader.load()
        feedbacks = data.find('ul', class_='list-reset feedbacks-new js-feedbacks-new js-comment-list')
        if feedbacks:
            for parser in self.parsers:
                parser.parse(feedbacks)
        else:
            print("Data not found")