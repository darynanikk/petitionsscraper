import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()


class PetitionsScraperPipeline:

    def __init__(self):
        self.con = psycopg2.connect(
            database=os.environ.get('DATABASE'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            host=os.environ.get('host'), port=os.environ.get('PORT')
        )
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
