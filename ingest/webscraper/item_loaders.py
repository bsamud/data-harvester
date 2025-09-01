from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from crawler.webscraper.items import WebScraperItem

class WebScraperItemLoader(ItemLoader):
    default_item_class = WebScraperItem
    default_output_processor = TakeFirst()
    content_out = Join()
