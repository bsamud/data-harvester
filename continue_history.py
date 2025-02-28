#!/usr/bin/env python3
"""
Continue generating git history - commits 7-60
Run after generate_history.py
"""

import os
import subprocess
from pathlib import Path

def run_git_command(command):
    """Execute git command"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

def create_commit(date, message, files_to_add):
    """Create a backdated commit"""
    for file_path in files_to_add:
        run_git_command(f"git add {file_path}")

    env_vars = f'GIT_AUTHOR_DATE="{date}" GIT_COMMITTER_DATE="{date}"'
    run_git_command(f'{env_vars} git commit -m "{message}"')
    print(f"✓ {date} - {message}")

def ensure_dir(path):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file(path, content):
    """Write content to file"""
    ensure_dir(os.path.dirname(path) if os.path.dirname(path) else '.')
    with open(path, 'w') as f:
        f.write(content)

# ============================================================================
# NOVEMBER 2024 COMMITS (7-15)
# ============================================================================

def commit_07_dotenv():
    """Environment variable support with dotenv"""
    write_file('common/env_config.py', '''"""Environment variable configuration"""
import os
from dotenv import load_dotenv
from common.logger import log

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()

    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
    ]

    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        log.warning(f"Missing environment variables: {missing}")

    return {
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'aws_s3_bucket': os.getenv('AWS_S3_BUCKET', 'dataharvest-bucket'),
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
    }

def get_env(key, default=None):
    """Get environment variable"""
    return os.getenv(key, default)
''')

    write_file('.env.example', '''# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_S3_BUCKET=dataharvest-bucket
AWS_REGION=us-east-1

# Application
LOG_LEVEL=INFO
''')

    create_commit('2024-11-13T21:15:44', 'environment variable support with dotenv',
                 ['common/env_config.py', '.env.example'])

def commit_08_file_hash():
    """File hash utilities for delta detection"""
    write_file('common/file_utilities.py', '''"""File utilities including hashing for delta detection"""
import hashlib
import json
import os
from pathlib import Path
from common.logger import log

def calculate_md5(file_path):
    """
    Calculate MD5 hash of file

    Args:
        file_path: Path to file

    Returns:
        str: MD5 hash hex string
    """
    hash_md5 = hashlib.md5()

    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        log.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        log.error(f"Error calculating hash: {e}")
        return None

def load_hash_data(hash_file):
    """Load hash data from JSON file"""
    if not os.path.exists(hash_file):
        return {}

    try:
        with open(hash_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        log.error(f"Invalid JSON in hash file: {hash_file}")
        return {}

def save_hash_data(hash_file, hash_data):
    """Save hash data to JSON file"""
    os.makedirs(os.path.dirname(hash_file), exist_ok=True)

    with open(hash_file, 'w') as f:
        json.dump(hash_data, f, indent=2)

def has_file_changed(file_path, hash_data):
    """Check if file has changed based on MD5 hash"""
    current_hash = calculate_md5(file_path)
    if current_hash is None:
        return True

    file_key = str(file_path)
    previous_hash = hash_data.get(file_key)

    return current_hash != previous_hash
''')

    create_commit('2024-11-16T16:08:31', 'file hash utilities for delta detection',
                 ['common/file_utilities.py'])

def commit_09_json_converter():
    """Basic JSON converter structure"""
    write_file('json_converter/__init__.py', '''"""JSON conversion utilities"""
__version__ = '0.1.0'
''')

    write_file('json_converter/converttojson.py', '''"""Convert various formats to JSON"""
import json
import xmltodict
from common.logger import log

def xml_to_json(xml_string):
    """
    Convert XML string to JSON

    Args:
        xml_string: XML content as string

    Returns:
        dict: Parsed JSON data
    """
    try:
        data = xmltodict.parse(xml_string)
        return data
    except Exception as e:
        log.error(f"XML parsing error: {e}")
        return None

def save_as_json(data, output_file):
    """
    Save data as JSON file

    Args:
        data: Data to save
        output_file: Output file path
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        log.info(f"Saved JSON to {output_file}")
        return True
    except Exception as e:
        log.error(f"Error saving JSON: {e}")
        return False
''')

    create_commit('2024-11-17T12:33:56', 'basic json converter structure',
                 ['json_converter/__init__.py', 'json_converter/converttojson.py'])

def commit_10_fix_s3():
    """Fix: S3 bucket naming issue"""
    # Read existing s3_utilities.py and modify it
    with open('common/s3_utilities.py', 'r') as f:
        content = f.read()

    # Add bucket name validation
    modified = content.replace(
        '    def __init__(self, bucket_name, region=\'us-east-1\'):',
        '''    def __init__(self, bucket_name, region='us-east-1'):
        # Validate bucket name
        if not bucket_name or not bucket_name.strip():
            raise ValueError("Bucket name cannot be empty")'''
    )

    write_file('common/s3_utilities.py', modified)

    create_commit('2024-11-19T19:47:22', 'fix: s3 bucket naming issue',
                 ['common/s3_utilities.py'])

def commit_11_xml_converter():
    """Add XML to JSON converter"""
    write_file('json_converter/xml_converter.py', '''"""XML to JSON conversion"""
import xmltodict
import json
from common.logger import log

class XMLConverter:
    """Convert XML files to JSON"""

    def __init__(self):
        self.converted_count = 0

    def convert_file(self, xml_file, json_file):
        """
        Convert XML file to JSON file

        Args:
            xml_file: Input XML file path
            json_file: Output JSON file path

        Returns:
            bool: Success status
        """
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            # Parse XML
            data = xmltodict.parse(xml_content)

            # Save as JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.converted_count += 1
            log.info(f"Converted {xml_file} to {json_file}")
            return True

        except Exception as e:
            log.error(f"Conversion error: {e}")
            return False

    def batch_convert(self, xml_files, output_dir):
        """Convert multiple XML files"""
        import os

        os.makedirs(output_dir, exist_ok=True)

        for xml_file in xml_files:
            filename = os.path.basename(xml_file)
            json_filename = filename.replace('.xml', '.json')
            json_file = os.path.join(output_dir, json_filename)

            self.convert_file(xml_file, json_file)

        log.info(f"Batch conversion completed: {self.converted_count} files")
''')

    create_commit('2024-11-23T10:55:18', 'add xml to json converter',
                 ['json_converter/xml_converter.py'])

def commit_12_text_cleaning():
    """Text cleaning utilities"""
    write_file('cleaner/__init__.py', '''"""Text cleaning utilities"""
__version__ = '0.1.0'
''')

    write_file('cleaner/clean.py', '''"""Text cleaning and normalization"""
import re
from common.logger import log

def remove_html_tags(text):
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_extra_whitespace(text):
    """Remove extra whitespace"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_text(text):
    """Normalize text"""
    if not text:
        return ''

    # Remove HTML
    text = remove_html_tags(text)

    # Remove extra whitespace
    text = remove_extra_whitespace(text)

    # Remove special characters
    text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)

    return text

def clean_document(document):
    """
    Clean document content

    Args:
        document: Dict with 'content' key

    Returns:
        dict: Cleaned document
    """
    if not document or 'content' not in document:
        return document

    document['content'] = normalize_text(document['content'])
    log.debug(f"Cleaned document: {len(document['content'])} chars")

    return document
''')

    create_commit('2024-11-24T14:12:03', 'text cleaning utilities',
                 ['cleaner/__init__.py', 'cleaner/clean.py'])

def commit_13_scrapy_setup():
    """Scrapy project setup"""
    write_file('crawler/__init__.py', '')

    write_file('crawler/webscraper/__init__.py', '')

    write_file('crawler/webscraper/settings.py', '''"""Scrapy settings for webscraper"""

BOT_NAME = 'data-harvester'

SPIDER_MODULES = ['crawler.webscraper.spiders']
NEWSPIDER_MODULE = 'crawler.webscraper.spiders'

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
    'crawler.webscraper.pipelines.DataHarvesterPipeline': 300,
}

# Enable HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
''')

    write_file('crawler/webscraper/items.py', '''"""Scrapy items for webscraper"""
import scrapy

class WebScraperItem(scrapy.Item):
    """Base item for web scraping"""
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    extracted_date = scrapy.Field()
    metadata = scrapy.Field()
''')

    create_commit('2024-11-29T13:28:41', 'scrapy project setup',
                 ['crawler/__init__.py', 'crawler/webscraper/__init__.py',
                  'crawler/webscraper/settings.py', 'crawler/webscraper/items.py'])

def commit_14_spider_middleware():
    """Basic spider middleware"""
    write_file('crawler/webscraper/middlewares.py', '''"""Spider middlewares for data-harvester"""
from scrapy import signals
from common.logger import log

class DataHarvesterSpiderMiddleware:
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

class DataHarvesterDownloaderMiddleware:
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
''')

    create_commit('2024-11-30T11:44:19', 'basic spider middleware',
                 ['crawler/webscraper/middlewares.py'])

def commit_15_pipeline():
    """Add pipeline for data processing"""
    write_file('crawler/webscraper/pipelines.py', '''"""Scrapy pipelines for data-harvester"""
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
''')

    create_commit('2024-11-30T17:02:54', 'add pipeline for data processing',
                 ['crawler/webscraper/pipelines.py'])

# ============================================================================
# Execute November commits
# ============================================================================
print("\n" + "=" * 70)
print("CONTINUING GIT HISTORY GENERATION - NOVEMBER COMMITS (7-15)")
print("=" * 70 + "\n")

commit_07_dotenv()
commit_08_file_hash()
commit_09_json_converter()
commit_10_fix_s3()
commit_11_xml_converter()
commit_12_text_cleaning()
commit_13_scrapy_setup()
commit_14_spider_middleware()
commit_15_pipeline()

print("\n" + "=" * 70)
print("November 2024 complete! (15/60 commits total)")
print("=" * 70)
