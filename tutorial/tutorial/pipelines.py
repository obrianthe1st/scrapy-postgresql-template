# pipelines.py

import psycopg2

class TutorialPipeline:

    def __init__(self):
        ## Connection Details
        hostname = ''
        username = ''
        password = '' # your password
        database = ''

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes(
            id serial PRIMARY KEY, 
            content text,
            tags text,
            author VARCHAR(255)
        )
        """)

    def process_item(self, item, spider):

        ## Check to see if text is already in database 
        self.cur.execute("select * from quotes where content = %s", (item['text'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['text'])


        ## If text isn't in the DB, insert data
        else:

            ## Define insert statement
            self.cur.execute(""" insert into quotes (content, tags, author) values (%s,%s,%s)""", (
                item["text"],
                str(item["tags"]),
                item["author"]
            ))

            ## Execute insert of data into database
            self.connection.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()