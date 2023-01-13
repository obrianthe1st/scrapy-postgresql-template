import scrapy
from ..items import TutorialItem
from scrapy.spiders import CrawlSpider

from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess

class BookSpider(scrapy.Spider):
    name = 'bookscraper'
    # start_urls = [
    #     'https://books.toscrape.com/catalogue/page-2.html',
    # ]

    #this methodology helps us to bypass the scraper
    url = 'https://books.toscrape.com/catalogue/page-{}.html'
    base_url = 'https://books.toscrape.com/'

    def start_requests(self):
        for i in range(1,3):
            yield scrapy.Request(self.url.format(i),
                                 meta={'playwright':True,
                                       'playwright_include_page': True,})


    def parse(self,response):
        items = TutorialItem()

        bookTitles = response.xpath('//article')
        for book in bookTitles:
            link = book.xpath('h3/a/@href').get()
            new_url = self.base_url +"catalogue/"+ link
            yield scrapy.Request(new_url,callback=self.parse_title)

    def parse_title(self,response):
        title = response.xpath('//div[@class="content"]//article//h1/text()').extract()
        yield {"title":title}

            





    
if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "CONCURRENT_REQUESTS": 32,
            "FEED_URI":'Products.jl',
            "FEED_FORMAT":'jsonlines',
        }
    )
    process.crawl(BookSpider)
    process.start()


