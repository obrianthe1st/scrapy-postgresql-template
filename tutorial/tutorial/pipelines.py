# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os

class TutorialPipeline:

    def __init__(self):
        #database details, use environment variables if I will ever upload these items
        hostname = ""
        username = ""
        password = ""
        database = ""
        port = ""

         ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database,port=port)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create books table if none exists, you can customize and create your own table in postgres
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books_to_read(
                id serial PRIMARY KEY, 
                title text,
                born text
            )""")



    def process_item(self, item, spider):

        ## Check to see if text is already in database 
        self.cur.execute("select * from books_to_read where title = %s", (item['title'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:
            ## Define insert statement
            self.cur.execute(""" insert into books_to_read (title, born) values (%s,%s)""", (
                item["title"],
                item["born"]
            ))

            ## Execute insert of data into database
            self.connection.commit()
            return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()