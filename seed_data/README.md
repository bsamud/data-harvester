# Seed Data

Sample datasets for testing and demonstration purposes.

## Contents

### web_content/
- **articles.json** - 15 tech articles with metadata (author, date, tags, word count)
- **blog_posts.json** - 10 developer blog posts with engagement metrics

### technical_docs/
- **api_documentation.json** - 8 REST API endpoint specifications
- **user_guides.json** - 5 product documentation guides with sections

### ecommerce/
- **products.json** - 20 product listings with specs, pricing, ratings
- **reviews.json** - 30 customer reviews with ratings and helpful votes

## Usage

```python
import json
from pathlib import Path

# Load articles
with open('seed_data/web_content/articles.json') as f:
    articles = json.load(f)

# Use with DataAggregator
from aggregate.data import DataAggregator
aggregator = DataAggregator()
data = aggregator.load_json_files(['seed_data/web_content/articles.json'])
```

## Data Schema

All files use consistent schemas suitable for:
- Text extraction and NLP testing
- Classification model training
- Data pipeline validation
- Demo and documentation examples
