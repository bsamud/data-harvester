"""Scrapy pipelines for data-harvester"""
from datetime import datetime
import json
from common.logger import log

class DataHarvesterPipeline:
    """Pipeline for processing scraped items"""

    def __init__(self):
        self.items_processed = 0
        self.items_dropped = 0

    def open_spider(self, spider):
        """Called when spider is opened"""
        log.info(f"Pipeline opened for spider: {spider.name}")
        self.items_processed = 0
        self.items_dropped = 0

    def close_spider(self, spider):
        """Called when spider is closed"""
        log.info(f"Pipeline closed: {self.items_processed} processed, {self.items_dropped} dropped")

    def process_item(self, item, spider):
        """Process scraped item"""
        # Add processing timestamp
        item['processed_date'] = datetime.now().isoformat()

        # Validate required fields
        if not item.get('url') or not item.get('content'):
            self.items_dropped += 1
            log.warning(f"Dropped item missing required fields")
            return None

        self.items_processed += 1
        log.debug(f"Processed item from: {item['url']}")

        return item
