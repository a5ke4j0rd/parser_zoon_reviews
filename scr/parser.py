import bs4.element
import requests
from bs4 import BeautifulSoup


def get_text_review(html_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('ul', class_='list-reset feedbacks-new js-feedbacks-new js-comment-list')

    for review_cards in data:
        if isinstance(review_cards, bs4.element.Tag):
            review_content = review_cards.find('div', class_='comment-item__container js-comment-container')

            if isinstance(review_content, bs4.element.Tag):
                review_text = review_content.find('span', class_='js-comment-content')
                print(review_text.text)
            else:
                continue

        else:
            continue
    return

if __name__ == '__main__':
    url = input('Enter URL: ')  # 'https://zoon.ru/msk/medical/meditsinskij_tsentr_sanprovi/'
    text = get_text_review(url)
    print(text)

