from parser import Parser
from db import kz_db
from telegram import send_telegram

if __name__ == '__main__':
    kz_parser = Parser("little brazil", '/Users/mac/Desktop/chromedriver')
    kz_db.connect()
    for i in kz_parser.get_review_ya('https://yandex.kz/maps/org/15161447173/reviews')[:5]:
        res = kz_parser.parse_review_ya(i)
        if not kz_db.search_id(res['review_id']):
            kz_db.insert(res)
            send_telegram(kz_parser.get_message(res))
    kz_db.connect.commit()
    kz_db.close()
