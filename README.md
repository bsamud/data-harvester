# dataHarvest

A generic, open-source data harvesting and ETL framework.

## Features
- Web scraping with Scrapy
- Data extraction and transformation
- ML-based classification
- NLP entity extraction
- Cloud storage (S3) integration
- Plugin architecture

## Installation
```bash
pip install -r requirements.txt
```

## Quick Start
```python
from common.logger import log
from common.app_config import get_config

config = get_config()
log.info("dataHarvest initialized")
```

## License
MIT
