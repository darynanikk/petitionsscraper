import sqlite3


class PetitionsscraperPipeline:
   
    def __init__(self):
        self.con = sqlite3.connect('storage.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS 
                         petitions_infos 
                         (number INTEGER, name TEXT, date TEXT)
                         """)
    
    def process_item(self, item, spider):
        self.cur.execute("SELECT * FROM petitions_infos WHERE name = ?", (item['name'],))
        result = self.cur.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['name'])
        else:
            self.cur.execute("""
                INSERT INTO petitions_infos (number, name, date) VALUES (?, ?, ?)
            """,
            (
                item['number'],
                item['name'],
                item['date']
            ))

            self.con.commit()
            return item