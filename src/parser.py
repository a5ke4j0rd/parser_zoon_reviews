import requests
import json
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
        return [star.text.strip() for star in stars]


class AuthorParser(DataParser):
    def parse(self, data):
        authors = data.find_all('span', {'itemscope': '', 'itemtype': 'https://schema.org/Person'})
        return [author.find('span').text.strip() for author in authors]

class ReviewParser(DataParser):
    def parse(self, data):
        reviews = data.find_all('div', {'data-uitest': 'comment-details-text'})
        return [review.find('span', class_='js-comment-content').text.strip() for review in reviews]

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
            results = {}
            stars = self.parsers[0].parse(feedbacks)
            authors = self.parsers[1].parse(feedbacks)
            reviews = self.parsers[2].parse(feedbacks)

            for i, (author, star, review) in enumerate(zip(authors, stars, reviews), 1):
                results[i] = [author, star, review]

            with open('reviews.json', 'w', encoding='utf-8') as reviews_json:
                json.dump(results, reviews_json, ensure_ascii=False, indent=4)
        else:
            print("Data not found")