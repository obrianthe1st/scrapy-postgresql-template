import scrapy
from ..items import TutorialItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

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

        # next_page = response.xpath('//nav/ul/li[@class="next"]/a/@href').get()
        next_page = f'https://quotes.toscrape.com/page/{QuotesSpider.page_number}/'

        if QuotesSpider.page_number < 11:
            QuotesSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
