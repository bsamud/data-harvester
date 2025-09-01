import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'

    def parse(self, response):
        yield {
            'url': response.url,
            'title': response.css('title::text').get()
        }
