import bs4.element
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

    def _get_author(self):
        data = self.__get_response()
        if data:
            reviews = data.find_all('div', class_='z-text--16 z-text--bold')
            for review in reviews:
                review_text = review.find('span', {'itemprop': 'name'}).text.strip()
                print(review_text)
        else:
            print("Отзывы не найдены.")

    def _get_text_review(self):
        data = self.__get_response()
        if data:
            reviews = data.find_all('div', {'data-uitest': 'comment-details-text'})
            for review in reviews:
                review_text = review.find('span', class_='js-comment-content').text.strip()
                print(review_text)
        else:
            print("Отзывы не найдены.")
