from parser import Parser
from db import kz_db
from telegram import send_telegram


def lets_start():
    kz_parser = Parser("little brazil", '/Users/mac/Desktop/chromedriver')
    kz_db.connect()
    kz_parser.get_all_rev()
    for item in kz_parser.reviews_query:
        if not kz_db.search_id(item['review_id']):
            kz_db.insert(item)
            send_telegram(kz_parser.get_message(item))
    kz_db.connect.commit()
    kz_db.close()


if __name__ == '__main__':
    lets_start()
