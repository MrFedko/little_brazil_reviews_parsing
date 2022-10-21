from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from db import kz_db
from telegram import send_telegram


class Parser:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_review_ya(self, url):
        ser = Service(self.path)
        op = webdriver.ChromeOptions()
        # op.add_argument('headless')
        op.add_argument('--no-sandbox')
        browser = webdriver.Chrome(service=ser, options=op)
        browser.implicitly_wait(5)
        url_rest = url
        browser.get(url_rest)
        browser.maximize_window()
        browser.find_element(By.CLASS_NAME, "rating-ranking-view").click()
        browser.find_element(By.CSS_SELECTOR, "body > div.popup._type_map-hint._position_bottom > div > div:nth-child(2) > div > div:nth-child(2)").click()
        sleep(4)
        source_data = browser.page_source
        soup = BeautifulSoup(source_data, features="html.parser")
        reviews = soup.find_all('div', {'class': 'business-reviews-card-view__review'})
        return reviews

    def parse_review_ya(self, review):
        date_time = ''
        id_review = ''
        author_name = ''
        author_url = ''
        rating = 0
        text = ''

        date_tr = review.find('span', {'class': 'business-review-view__date'})
        date = str(date_tr.find('meta')).split()[1].split('=')[1].split('T')[0].replace('"','')
        time = str(date_tr.find('meta')).split()[1].split('=')[1].split('T')[1][0:5]
        date_time = date + ' ' + time

        rating_tr = review.find('div', {'class': 'business-rating-badge-view__stars'})
        rating_tt = rating_tr.find_all('span', {'class': 'inline-image _loaded business-rating-badge-view__star _full _size_m'})
        for _ in rating_tt:
            rating += 1

        author_url_tr = review.find('a', {'class': 'business-review-view__user-icon'})
        author_url = str(author_url_tr).split()[3].split('"')[1]

        author_name = str(review.find('span', {'itemprop': 'name'})).split('>')[1].split('<')[0].replace("'", "")

        text = str(review.find('span', {'class': 'business-review-view__body-text'})).split('>')[1].split('<')[0].replace("'", "")

        id_review = str(review.find('span', {'class': 'business-review-view__date'}).find('meta')).split('"')[1]
        result = {'site': 'Yandex', 'date_time': date_time, 'review_id': id_review,
                  'author_name': author_name, 'author_url': author_url, 'rating': rating, 'text': text }
        return result

    def get_message(self, review_info):
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
