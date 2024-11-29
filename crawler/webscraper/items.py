"""Scrapy items for webscraper"""
import scrapy

class WebScraperItem(scrapy.Item):
    """Base item for web scraping"""
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    extracted_date = scrapy.Field()
    metadata = scrapy.Field()
