from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from info import parser_bot
from datetime import datetime


class Parser:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self._reviews_query = []

    def get_review_ya(self, url: str) -> str:
        ser = Service(self.path)
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument('--headless=new')
        op.add_argument('--no-sandbox')
        browser = webdriver.Chrome(service=ser, options=op)
        browser.implicitly_wait(5)
        browser.get(url)
        print("Open website Ya")
        browser.maximize_window()
        sleep(4)
        try:
            element = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "rating-ranking-view")))
            browser.execute_script("arguments[0].click();", element)
            print("Click on selector Ya")
            el2 = browser.find_element(By.CSS_SELECTOR,
                                       "body > div.popup._type_map-hint._position_bottom > div > div:nth-child(2) > div > div:nth-child(2)")
            browser.execute_script("arguments[0].click();", el2)
            print("Click on the newest reviews Ya")
            sleep(4)
        except Exception as e:
            print('Error in clicking BTN : ' + str(e))
        source_data = browser.page_source
        soup = BeautifulSoup(source_data, features="html.parser")
        reviews = soup.find_all('div', {'class': 'business-reviews-card-view__review'})
        browser.close()
        return reviews

    def parse_review_ya(self, review: str) -> dict:
        date_tr = review.find('span', {'class': 'business-review-view__date'})
        date = str(date_tr.find('meta')).split()[1].split('=')[1].split('T')[0].replace('"', '')
        time = str(date_tr.find('meta')).split()[1].split('=')[1].split('T')[1][0:5]
        date_time = date + ' ' + time

        rating_tr = review.find('div', {'class': 'business-rating-badge-view__stars'}) \
            .find_all('span',
                      {'class': 'inline-image _loaded business-rating-badge-view__star _full _size_m'})
        rating = len(rating_tr)

        author_url = str(review.find('a', {'class': 'business-review-view__user-icon'})).split()[3].split('"')[1]

        author_name = str(review.find('span', {'itemprop': 'name'})).split('>')[1].split('<')[0].replace("'", "")

        text = str(review.find('span', {'class': 'business-review-view__body-text'})).split('>')[1].split('<')[
            0].replace("'", "")

        id_review = str(review.find('span', {'class': 'business-review-view__date'}).find('meta')).split('"')[1]
        result = {'site': 'Yandex',
                  'date_time': date_time,
                  'review_id': id_review,
                  'author_name': author_name,
                  'author_url': author_url,
                  'rating': rating,
                  'text': text}
        return result

    def get_review_two_gis(self, url: str):
        ser = Service(self.path)
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        op.add_argument('--headless=new')
        op.add_argument('--no-sandbox')
        browser = webdriver.Chrome(service=ser, options=op)
        browser.implicitly_wait(5)
        browser.get(url)
        print("Open website 2Gis")
        browser.maximize_window()
        browser.save_screenshot("open_2gis.png")
        sleep(5)
        browser.save_screenshot('load_2gis.png')
        source_data = browser.page_source
        soup = BeautifulSoup(source_data, features="html.parser")
        reviews = soup.find_all('div', {'class': '_11gvyqv'})
        return reviews

    def parse_review_two_gis(self, review: str) -> dict:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        author_name = str(review.find('span', {'class': '_er2xx9'})).split('>')[2].split('<')[0]
        author_url = parser_bot.two_gis
        text = str(review.find('div', {'class': '_49x36f'})).split('>')[2].split('<')[0]
        rating = len(review.find('div', {'class': '_1fkin5c'}) \
                     .find_all('span', {'style': 'width:10px;height:10px'}))
        id_review = "".join([str(ord(i)) for i in author_name][:12]) + str(ord(text[0])) + str(rating)

        result = {'site': '2Gis',
                  'date_time': date_time,
                  'review_id': id_review,
                  'author_name': author_name,
                  'author_url': author_url,
                  'rating': rating,
                  'text': text}
        return result

    def get_review_google(self, url: str):
        print("Open website Google")
        response = requests.request("GET", url, headers={}, data={})
        result_google = response.json()
        print("Get reviews from Google")
        if 'result' in result_google:
            return result_google['result']['reviews']
        else:
            return None

    def parse_review_google(self, review: dict) -> (dict, None):
        if 'time' not in review:
            print(review)
            return None
        date_time = datetime.utcfromtimestamp(int(review['time'])).strftime('%Y-%m-%d %H:%M')
        author_name = review['author_name']
        author_url = review['author_url']
        text = review['text']
        id_review = datetime.utcfromtimestamp(int(review['time'])).strftime('%Y%m%d %H%M%S')
        rating = review['rating']

        result = {'site': 'Google',
                  'date_time': date_time,
                  'review_id': id_review,
                  'author_name': author_name,
                  'author_url': author_url,
                  'rating': rating,
                  'text': text}
        return result

    def get_message(self, review_info: dict) -> (str, None):
        if review_info is None:
            return None
        review_site = review_info['site']
        review_date = review_info['date_time']
        review_author_name = review_info['author_name']
        review_author_url = review_info['author_url']
        review_author = f'<a href="{review_author_url}">{review_author_name}</a>'
        rating = {1: '★✩✩✩✩',
                  2: '★★✩✩✩',
                  3: '★★★✩✩',
                  4: '★★★★✩',
                  5: '★★★★★'}
        review_rating = rating[review_info['rating']]
        review_text = review_info['text']

        message = f'''
        {review_rating}
        {review_site}, {review_date}
        автор: {review_author}
        
        {review_text}'''
        return message

    def get_all_rev(self):
        for ya, gis, google in zip((self.get_review_ya(parser_bot.yandex)[:5]),
                                   (self.get_review_two_gis(parser_bot.two_gis)[:5]),
                                   (self.get_review_google(parser_bot.google))):
            self._reviews_query.extend((self.parse_review_ya(ya),
                                        self.parse_review_two_gis(gis),
                                        self.parse_review_google(google)))

    @property
    def reviews_query(self):
        return self._reviews_query
