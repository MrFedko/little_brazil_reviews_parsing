import sqlite3


class DBConnector:
    def __init__(self, name):
        self.name = name

    def connect(self):
        self.connect = sqlite3.connect(self.name)
        print("Opened database successfully")

    def close(self):
        self.connect.close()
        print("Closed database successfully")

    def create_table(self):
        self.connect()
        self.connect.execute("""CREATE TABLE reviews
                                (ID         INTEGER PRIMARY KEY AUTOINCREMENT, 
                                SITE        VARCHAR(10),
                                DATETIME    TEXT,
                                REVIEW_ID   TEXT            FOREIGN_KEY,
                                AUTHOR_NAME TEXT,
                                URL         TEXT,
                                RATING      INT,
                                BODY        TEXT,
                                SENT        INT         DEFAULT 0);""")
        print("Table reviews  successfully created")
        self.close()

    def insert(self, review):
        info = list(review.values())
        print(info)
        self.connect.execute(f"""INSERT INTO reviews (SITE, DATETIME, REVIEW_ID, AUTHOR_NAME, URL, RATING, BODY)
                                VALUES('{info[0]}', '{info[1]}', '{info[2]}', '{info[3]}', '{info[4]}', {info[5]}, '{info[6]}');""")

    def search_id(self, id):
        cursor = self.connect.execute(f"""SELECT REVIEW_ID FROM reviews
                                WHERE REVIEW_ID = '{id}';""")
        for row in cursor:
            return row[0] == id


kz_db = DBConnector("reviews_kz.db")
# kz_db.create_table()


