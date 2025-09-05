# data-harvester

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modular, open-source data harvesting and ETL framework.

## Features

- **Ingest** - Web scraping with Scrapy
- **Extract** - PDF text extraction and NLP entity recognition (spaCy)
- **Classify** - ML-based document classification (scikit-learn)
- **Scrub** - Text cleaning and normalization
- **Enrich** - Extensible data enrichment pipeline
- **Convert** - XML/JSON format conversion
- **Aggregate** - Multi-source data loading
- **Plugins** - Extensible plugin architecture
- **Cloud** - AWS S3 integration with caching

## Installation

```bash
pip install data-harvester
```

Or from source:

```bash
git clone https://github.com/bharatsamudrala/data-harvester.git
cd data-harvester
pip install -e .
```

## Quick Start

```bash
# Set up environment
cp .env.example .env
python -m spacy download en_core_web_sm

# Run
python harvest_main.py -c appconfig.ini -v
```

## Usage

```python
# Text cleaning
from scrub.clean import normalize_text
clean_text = normalize_text("<p>Hello World</p>")

# Entity extraction
from extract.extract import EntityExtractor
extractor = EntityExtractor()
entities = extractor.extract_entities("Apple Inc. is in Cupertino.")

# Document classification
from classify.classify import DocumentClassifier
classifier = DocumentClassifier()
classifier.train(texts, labels)
predictions = classifier.predict(new_texts)

# Parallel processing
from common.parallel_processor import ParallelProcessor
processor = ParallelProcessor(num_workers=4)
results = processor.process_batch(my_function, items)
```

## Project Structure

```
data-harvester/
  ingest/        # Web scraping (Scrapy)
  extract/       # NLP & PDF extraction
  classify/      # ML classification
  scrub/         # Text cleaning
  enrich/        # Data enrichment
  convert/       # Format conversion
  aggregate/     # Data loading
  common/        # Shared utilities
  plugins/       # Plugin system
  benchmarks/    # Performance tests
  seed_data/     # Sample datasets
```

## Benchmarks

```bash
# Run all benchmarks
python benchmarks/run_benchmarks.py

# Quick benchmark
python benchmarks/run_benchmarks.py --quick
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Plugin Development](docs/PLUGIN_DEVELOPMENT.md)

## License

MIT

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
