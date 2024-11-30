"""Spider middlewares for dataHarvest"""
from scrapy import signals
from common.logger import log

class DataHarvestSpiderMiddleware:
    """Spider middleware for custom processing"""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """Process spider input"""
        return None

    def process_spider_output(self, response, result, spider):
        """Process spider output"""
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """Handle spider exceptions"""
        log.error(f"Spider exception: {exception}")
        pass

    def spider_opened(self, spider):
        """Called when spider is opened"""
        log.info(f"Spider opened: {spider.name}")

class DataHarvestDownloaderMiddleware:
    """Downloader middleware"""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """Process download request"""
        return None

    def process_response(self, request, response, spider):
        """Process download response"""
        return response

    def process_exception(self, request, exception, spider):
        """Handle download exceptions"""
        log.error(f"Download exception: {exception}")
        pass

    def spider_opened(self, spider):
        """Called when spider is opened"""
        log.info(f"Downloader middleware active for: {spider.name}")
