"""Scrapy settings for webscraper"""

BOT_NAME = 'data-harvester'

SPIDER_MODULES = ['ingest.webscraper.spiders']
NEWSPIDER_MODULE = 'ingest.webscraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16

# Configure a delay for requests
DOWNLOAD_DELAY = 1

# Disable cookies
COOKIES_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
    'ingest.webscraper.pipelines.DataHarvesterPipeline': 300,
}

# Enable HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
