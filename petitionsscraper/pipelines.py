import psycopg2
import os

from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values()

DEBUG = bool(config.get('DEBUG'))
DATABASE_URL = os.environ['DATABASE_URL']

db_credentials = {
    'database': 'petitions_info',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': 5432
}


class PetitionsScraperPipeline:

    def __init__(self):
        if DEBUG:
            self.con = psycopg2.connect(**db_credentials)
        self.con = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.con.autocommit = True
        self.cur = self.con.cursor()
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS 
                         petitions
                         (order_number int, name varchar(55), date varchar(55))
                         """)

    def process_item(self, item, spider):
        self.cur.execute("SELECT * FROM petitions WHERE name = %s", (item['name'],))
        result = self.cur.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['name'])
        else:
            self.cur.execute("INSERT INTO petitions VALUES (%s, %s, %s)",
                             (
                                 item['order_number'],
                                 item['name'],
                                 item['date']
                             ))

            self.con.commit()
            return item
