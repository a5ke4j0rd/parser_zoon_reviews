import requests
from bs4 import BeautifulSoup


class Parser:
    __headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    }

    def __init__(self, url):
        self.url = url

    def __get_response(self):
        response = requests.get(self.url, headers=Parser.__headers, timeout=5)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('ul', class_='list-reset feedbacks-new js-feedbacks-new js-comment-list')
        return data

    def _get_stars(self):
        data = self.__get_response()
        if data:
            stars = data.find_all('div', {'data-uitest':'personal-mark'})
            for star in stars:
                print(star.text)

    def _get_author(self):
        data = self.__get_response()
        if data:
            authors = data.find_all('span', {'itemscope':'', 'itemtype':'https://schema.org/Person'})
            for author in authors:
                author_name = author.find('span').text.strip()
                print(author_name)
        else:
            print("Authors not found")

    def _get_text_review(self):
        data = self.__get_response()
        if data:
            reviews = data.find_all('div', {'data-uitest': 'comment-details-text'})
            for review in reviews:
                review_text = review.find('span', class_='js-comment-content').text.strip()
                print(review_text)
        else:
            print("Reviews not found")
