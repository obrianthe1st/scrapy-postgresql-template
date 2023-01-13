import scrapy
from ..items import TutorialItem

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess

class QuotesSpider(CrawlSpider):
    name = 'books_crawl_spider'


    start_urls = ['https://quotes.toscrape.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="quote"]/span/a'),callback='parse_item',follow=True),
        # Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a')),
        )

    def parse_item(self,response):
        item = TutorialItem()

        born = f" {response.xpath('//h3/following-sibling::p[1]/span[1]/text()').get()}, {response.xpath('//h3/following-sibling::p[1]/span[2]/text()').get()}" 

        item['title'] = response.xpath('normalize-space(//h3/text())').get()
        item['born'] = born

        yield item
     

    
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


