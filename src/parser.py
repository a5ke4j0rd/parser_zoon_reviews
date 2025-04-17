import requests
import json
import random
import time
from datetime import datetime
from decouple import config
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class HtmlLoader:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": UserAgent().random
        }
        self.proxy = self._get_proxy()


    # --- LOADING PROXYS ---

    def _get_proxy(self):
        try:
            proxies = config('PROXY', default='')
            return {"http": f"socks5://{proxies}", "https": f"socks5://{proxies}"}
        except Exception as e:
            print(f"Proxy error: {e}")
        return None

    def __check_proxy_connection(self):
        try:
            test_url = "https://api.ipify.org?format=json"
            response = requests.get(test_url,
                                    proxies=self.proxy,
                                    timeout=10)
            ip_data = response.json()
            print(f"Current IP via proxy: {ip_data['ip']}")
            return True
        except Exception as e:
            print(f"Proxy not working! Error: {e}")
            return False


    # --- LOADING RESPONSE ---

    def load(self):
        # print(self.__check_proxy_connection()) FOR DEBUG
        time.sleep(random.uniform(2, 4))
        response = requests.get(self.url, headers=self.headers,
                                proxies=self.proxy, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')


class Parser:
    def __init__(self, url):
        self.loader = HtmlLoader(url)
        self.parsers = [
            self._parse_stars,
            self._parse_authors,
            self._parse_dates,
            self._parse_reviews
        ]


    # --- RATING PARSER METHOD ---

    def _parse_stars(self, data):
        return [s.text.strip() for s in
                data.find_all('div', {'data-uitest': 'personal-mark'})]


    # --- AUTHOR PARSER METHOD ---

    def _parse_authors(self, data):
        return [
            a.find('span').text.strip() for a in
            data.find_all('strong', class_='comment-item__header-name')
            if not a.find('a', attrs={'itemtype': 'https://schema.org/Organization'})
               and a.find('span')
        ]


    # --- DATE PARSER METHOD ---

    def _parse_dates(self, data):
        dates = []
        for review in data.find_all('li', class_='comment-item js-comment'):
            date_tag = review.find('meta', {'itemprop': 'datePublished'})
            if date_tag and 'content' in date_tag.attrs:
                try:
                    date = datetime.fromisoformat(date_tag['content']).date()
                    dates.append(str(date))
                except ValueError:
                    dates.append(None)
            else:
                dates.append(None)
        return dates


    # --- REVIEW PARSER METHOD ---

    def _parse_reviews(self, data):
        reviews = []
        for review in data.find_all('li', class_='comment-item js-comment'):
            if not review.get('data-id'):
                continue

            content = None
            for part in review.find_all('div', class_='js-comment-part'):
                subtitle = part.find('div', class_='comment-text-subtitle')
                text = part.find('span', class_='js-comment-content')

                if not subtitle or not text:
                    continue

                if 'Достоинства' in subtitle.text:
                    content = f"Достоинства: {text.text.strip()}"
                    break
                elif 'Комментарий' in subtitle.text and not content:
                    content = f"Комментарий: {text.text.strip()}"

            if content:
                reviews.append(content)
        return reviews


    # --- MAIN PARSER METHOD ---

    def run(self):
        soup = self.loader.load()
        feedbacks = soup.find('ul', class_='feedbacks-new')

        if not feedbacks:
            print("No reviews found")
            return

        parsed_data = [parser(feedbacks) for parser in self.parsers]

        results = {
            i: {
                "rating": rating,
                "author": author,
                "date": date,
                "review": review
            }
            for i, (rating, author, date, review) in enumerate(
                zip(*parsed_data), 1)
        }

        with open('reviews.json', 'w', encoding='utf-8') as reviews:
            json.dump(results, reviews, ensure_ascii=False, indent=2)
