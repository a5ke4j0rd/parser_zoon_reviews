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
        data = soup.find('div', class_='service-block-content')
        return data

    def _get_author(self):
        data = self.__get_response()

        for review_cards in data:
            if isinstance(review_cards, bs4.element.Tag):
                review_content = review_cards.find('div', class_='comment-item__wrapper js-comment-container-wrapper')

                if isinstance(review_content, bs4.element.Tag):
                    review_text = review_content.find('span', class_='js-comment-content')
                    print(review_text.text)
                else:
                    continue
            else:
                continue
        return

    def _get_text_review(self):
        data = self.__get_response()
        for text in data:
                review_container = text.find('div', class_='comment-item__wrapper js-comment-container-wrapper')
                review_text = review_container.find('span', class_='js-comment-content').text # .split() - for search method
                print(review_text)