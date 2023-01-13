import scrapy
from ..items import TutorialItem

from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = 'books'
    page_number = 2
    # start_urls = [
    #     'https://quotes.toscrape.com/page/1/',
    # ]

    #this methodology helps us to bypass the scraper
    url = 'https://quotes.toscrape.com/page/{}/'

    def start_requests(self):
        for i in range(1,11):
            yield scrapy.Request(self.url.format(i),
                                 meta={'playwright':True,
                                       'playwright_include_page': True,})


    def parse(self,response):
        items = TutorialItem()

        divQuote = response.xpath('//div[@class="quote"]')
        for quote in divQuote:
            title = quote.xpath('span[@class="text"]/text()').extract()
            author = quote.xpath('span//small[@class="author"]/text()').extract()
            tags = quote.xpath('div[@class="tags"]//a/text()').extract()
            link = quote.xpath('span//a/@href').extract()
            
            items['title'] = title
            items['author'] = author
            items['tags'] = tags
            items['link'] = link

            yield items

    
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
    process.crawl(QuotesSpider)
    process.start()


