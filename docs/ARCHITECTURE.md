# data-harvester Architecture

This document provides a comprehensive overview of the data-harvester architecture using diagrams and detailed explanations.

## Table of Contents
- [System Architecture Overview](#system-architecture-overview)
- [Data Flow](#data-flow)
- [Component Interaction](#component-interaction)
- [Plugin System](#plugin-system)
- [ML/NLP Pipeline](#mlnlp-pipeline)
- [Configuration Management](#configuration-management)
- [Core Components](#core-components)

---

## System Architecture Overview

The following diagram shows the high-level architecture of data-harvester:

```mermaid
graph TB
    subgraph "Data Sources"
        WEB[Web Pages]
        PDF[PDF Documents]
        XML[XML Files]
        API[External APIs]
    end

    subgraph "Ingestion Layer"
        INGEST[Ingest Module<br/>Scrapy-based]
        PDF_EXT[PDF Extractor<br/>PyPDF2]
        XML_CONV[XML Converter<br/>xmltodict]
    end

    subgraph "Processing Layer"
        SCRUB[Scrub<br/>Text Normalization]
        EXTRACT[Entity Extractor<br/>spaCy NLP]
        ENRICH[Enrichment Pipeline<br/>Chain of Enrichers]
        CLASS[Document Classifier<br/>scikit-learn]
    end

    subgraph "Storage Layer"
        LOCAL[Local Storage<br/>JSON Files]
        S3[AWS S3<br/>Cloud Storage]
        CACHE[S3 Cache<br/>TTL-based]
    end

    subgraph "Common Services"
        CONFIG[Configuration<br/>INI/YAML/ENV]
        LOG[Logger<br/>Structured Logging]
        DELTA[Delta Detector<br/>MD5 Hashing]
        PARALLEL[Parallel Processor<br/>Multiprocessing]
    end

    WEB --> INGEST
    PDF --> PDF_EXT
    XML --> XML_CONV
    API --> INGEST

    INGEST --> SCRUB
    PDF_EXT --> SCRUB
    XML_CONV --> SCRUB

    SCRUB --> EXTRACT
    EXTRACT --> ENRICH
    ENRICH --> CLASS

    CLASS --> LOCAL
    CLASS --> S3
    S3 --> CACHE

    CONFIG -.-> INGEST
    CONFIG -.-> CLASS
    LOG -.-> INGEST
    LOG -.-> CLASS
    DELTA -.-> INGEST
    PARALLEL -.-> EXTRACT
```

---

## Data Flow

This diagram illustrates how data flows through the system from ingestion to storage:

```mermaid
flowchart LR
    subgraph INPUT["Input Stage"]
        direction TB
        A1[Web Scraping]
        A2[PDF Upload]
        A3[XML Import]
    end

    subgraph VALIDATE["Validation Stage"]
        direction TB
        B1[URL Validation]
        B2[Schema Validation]
        B3[Required Fields Check]
    end

    subgraph TRANSFORM["Transform Stage"]
        direction TB
        C1[HTML Tag Removal]
        C2[Whitespace Normalization]
        C3[Text Cleaning]
    end

    subgraph EXTRACT["Extraction Stage"]
        direction TB
        D1[Entity Extraction]
        D2[Metadata Extraction]
        D3[Content Parsing]
    end

    subgraph ENRICH["Enrichment Stage"]
        direction TB
        E1[Custom Enrichers]
        E2[Data Augmentation]
        E3[Cross-referencing]
    end

    subgraph CLASSIFY["Classification Stage"]
        direction TB
        F1[TF-IDF Vectorization]
        F2[Model Prediction]
        F3[Confidence Scoring]
    end

    subgraph OUTPUT["Output Stage"]
        direction TB
        G1[JSON Export]
        G2[S3 Upload]
        G3[DataFrame Output]
    end

    INPUT --> VALIDATE --> TRANSFORM --> EXTRACT --> ENRICH --> CLASSIFY --> OUTPUT
```

---

## Component Interaction

Detailed view of how modules interact with each other:

```mermaid
graph LR
    subgraph ingest["Ingest Module"]
        SPIDER[Spider]
        PIPELINE[Pipeline]
        ITEMS[Items]
    end

    subgraph extract["Extract Module"]
        ENT_EXT[EntityExtractor]
        PDF_EXT[PDFExtractor]
    end

    subgraph classify["Classifier Module"]
        DOC_CLASS[DocumentClassifier]
        TRAIN_PIPE[TrainingPipeline]
    end

    subgraph common["Common Module"]
        APP_CFG[AppConfig]
        S3_MGR[S3Manager]
        LOGGER[Logger]
        DELTA[DeltaDetector]
    end

    subgraph enrich["Enrich Module"]
        ENRICH_PIPE[EnrichmentPipeline]
    end

    subgraph aggregate["Aggregate Module"]
        AGGREGATOR[DataAggregator]
    end

    SPIDER --> PIPELINE
    PIPELINE --> ITEMS
    ITEMS --> ENT_EXT
    ITEMS --> DOC_CLASS

    PDF_EXT --> ENT_EXT
    ENT_EXT --> ENRICH_PIPE
    ENRICH_PIPE --> DOC_CLASS

    DOC_CLASS --> AGGREGATOR
    TRAIN_PIPE --> DOC_CLASS

    APP_CFG -.-> SPIDER
    APP_CFG -.-> S3_MGR
    S3_MGR -.-> AGGREGATOR
    LOGGER -.-> SPIDER
    LOGGER -.-> DOC_CLASS
    DELTA -.-> SPIDER
```

---

## Plugin System

The extensible plugin architecture:

```mermaid
graph TB
    subgraph "Plugin Framework"
        LOADER[Plugin Loader<br/>plugin_loader.py]
        BASE[Plugin Base Class<br/>plugin_base.py]
        REGISTRY[Plugin Registry]
    end

    subgraph "Plugin Configuration"
        YAML[plugin.yaml]
        APP_CFG[AppConfig]
    end

    subgraph "Example Plugins"
        EXAMPLE[Example Plugin]
        CUSTOM[Custom Plugin...]
    end

    subgraph "Plugin Lifecycle"
        INIT[initialize]
        PROCESS[process]
        OUTPUT[output]
    end

    YAML --> LOADER
    APP_CFG --> LOADER
    LOADER --> REGISTRY

    BASE --> EXAMPLE
    BASE --> CUSTOM

    REGISTRY --> EXAMPLE
    REGISTRY --> CUSTOM

    EXAMPLE --> INIT
    INIT --> PROCESS
    PROCESS --> OUTPUT
```

### Plugin Development Flow

```mermaid
sequenceDiagram
    participant User
    participant PluginLoader
    participant AppConfig
    participant Plugin
    participant DataPipeline

    User->>PluginLoader: Load plugins from config
    PluginLoader->>AppConfig: Get plugin configurations
    AppConfig-->>PluginLoader: Return plugin.yaml paths
    PluginLoader->>PluginLoader: Dynamic import (importlib)
    PluginLoader->>Plugin: Create plugin instance
    Plugin->>Plugin: initialize()
    PluginLoader-->>User: Plugin registry ready

    User->>DataPipeline: Process data
    DataPipeline->>Plugin: process(data)
    Plugin-->>DataPipeline: Processed data
    DataPipeline-->>User: Results
```

---

## ML/NLP Pipeline

### Document Classification Flow

```mermaid
flowchart TB
    subgraph "Training Phase"
        T1[Load Training Data] --> T2[Text Preprocessing]
        T2 --> T3[TF-IDF Vectorization]
        T3 --> T4[Train Naive Bayes]
        T4 --> T5[Cross Validation]
        T5 --> T6[Save Model]
    end

    subgraph "Prediction Phase"
        P1[New Document] --> P2[Text Preprocessing]
        P2 --> P3[Load Model]
        P3 --> P4[TF-IDF Transform]
        P4 --> P5[Predict Label]
        P5 --> P6[Confidence Score]
    end

    T6 -.-> P3
```

### Entity Extraction Pipeline

```mermaid
flowchart LR
    subgraph "Input"
        TEXT[Raw Text]
        PDF[PDF Document]
    end

    subgraph "Extraction"
        SPACY[spaCy NLP Model]
        NER[Named Entity Recognition]
    end

    subgraph "Output"
        ENTITIES[Entity List]
        GROUPED[Entities by Type]
    end

    TEXT --> SPACY
    PDF -->|PyPDF2| TEXT
    SPACY --> NER
    NER --> ENTITIES
    NER --> GROUPED
```

### Training Pipeline Sequence

```mermaid
sequenceDiagram
    participant Data as Training Data
    participant Pipeline as TrainingPipeline
    participant Classifier as DocumentClassifier
    participant Metrics as Evaluation

    Data->>Pipeline: load_data(file_path)
    Pipeline->>Pipeline: train_test_split (80/20)
    Pipeline->>Classifier: train(X_train, y_train)
    Classifier->>Classifier: fit TF-IDF + Naive Bayes
    Pipeline->>Classifier: predict(X_test)
    Classifier-->>Pipeline: predictions
    Pipeline->>Metrics: calculate metrics
    Metrics-->>Pipeline: accuracy, precision, recall, f1
    Pipeline->>Pipeline: cross_validate (5-fold)
    Pipeline->>Classifier: save_model(path)
```

---

## Configuration Management

```mermaid
graph TB
    subgraph "Configuration Sources"
        INI[appconfig.ini<br/>Main Config]
        ENV[.env<br/>Secrets]
        YAML[plugin.yaml<br/>Plugin Config]
    end

    subgraph "Configuration Layer"
        APP_CFG[AppConfig<br/>Singleton]
        ENV_CFG[EnvConfig<br/>dotenv]
        YAML_CFG[YamlConfig<br/>PyYAML]
    end

    subgraph "Consumers"
        INGEST[Ingest]
        S3[S3Manager]
        CLASSIFIER[Classifier]
        PLUGINS[Plugins]
    end

    INI --> APP_CFG
    ENV --> ENV_CFG
    YAML --> YAML_CFG

    ENV_CFG --> APP_CFG
    YAML_CFG --> APP_CFG

    APP_CFG --> INGEST
    APP_CFG --> S3
    APP_CFG --> CLASSIFIER
    APP_CFG --> PLUGINS
```

### Configuration Loading Sequence

```mermaid
sequenceDiagram
    participant Main as harvest_main.py
    participant AppConfig
    participant EnvConfig
    participant Components

    Main->>EnvConfig: load_environment()
    EnvConfig->>EnvConfig: Load .env file
    EnvConfig-->>Main: Environment ready

    Main->>AppConfig: get_config(path)
    AppConfig->>AppConfig: Parse INI file
    AppConfig->>AppConfig: Load plugin configs
    AppConfig-->>Main: Config singleton

    Main->>Components: Initialize with config
    Components->>AppConfig: get(section, key)
    AppConfig-->>Components: Configuration values
```

---

## Core Components

### 1. Common Utilities
- **Configuration management** - INI, YAML, and environment variable support
- **Logging** - Structured logging with console and file handlers
- **S3 operations** - Upload, download, list, and cache S3 objects
- **File utilities** - MD5 hashing and delta detection

### 2. Data Processing
- **JSON/XML converters** - Format transformation utilities
- **Text cleaning** - HTML removal, whitespace normalization
- **Delta detection** - Track file changes using MD5 hashing
- **Aggregation** - Combine data from multiple sources

### 3. ML/NLP
- **Classification** - scikit-learn based document classification
- **Entity extraction** - spaCy Named Entity Recognition
- **Training pipelines** - Model training and evaluation workflows

### 4. Web Scraping
- **Scrapy integration** - Configurable web crawling
- **Middleware** - Request/response processing
- **Pipelines** - Item validation and processing

### 5. Plugin System
- **Plugin loader** - Dynamic plugin loading from YAML config
- **Plugin base class** - Abstract base for custom plugins
- **Example plugins** - Reference implementations

---

## Processing Pseudocode

### Main Harvest Process

```
FUNCTION harvest_data(config_path, process_id):
    # Initialize
    config = load_config(config_path)
    logger = setup_logger(config)

    # Load plugins if configured
    plugins = load_plugins(config)

    # Initialize components
    ingest = initialize_ingest(config)
    extractor = EntityExtractor()
    classifier = DocumentClassifier()

    # Load pre-trained model if exists
    IF model_exists(config.model_path):
        classifier.load_model(config.model_path)

    # Main processing loop
    FOR source IN config.sources:
        # Crawl/fetch data
        raw_data = ingest.crawl(source)

        # Check for changes
        IF delta_detector.has_changed(raw_data):
            # Clean text
            cleaned = scrub.normalize_text(raw_data)

            # Extract entities
            entities = extractor.extract_entities(cleaned)

            # Apply enrichers
            FOR enricher IN enrichment_pipeline:
                cleaned = enricher.enrich(cleaned)

            # Classify document
            label = classifier.predict(cleaned)

            # Apply plugin processing
            FOR plugin IN plugins:
                cleaned = plugin.process(cleaned)

            # Store results
            IF config.use_s3:
                s3_manager.upload(cleaned)
            ELSE:
                save_to_local(cleaned)

    RETURN success
```

### Batch Processing with Parallelization

```
FUNCTION process_batch(items, processor_func):
    # Determine worker count
    num_workers = min(cpu_count(), len(items))

    # Create process pool
    WITH ProcessPoolExecutor(num_workers) AS pool:
        # Map function across items
        results = pool.map(processor_func, items)

    RETURN list(results)
```

---

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development"
        DEV[Developer Machine]
        LOCAL_FS[Local Filesystem]
    end

    subgraph "AWS Cloud"
        S3[S3 Bucket<br/>dataharvest-bucket]

        subgraph "Optional"
            LAMBDA[Lambda Functions]
            SQS[SQS Queue]
        end
    end

    subgraph "Data Sources"
        WEB[Web Sources]
        DOCS[Document Stores]
    end

    DEV --> LOCAL_FS
    DEV --> S3
    WEB --> DEV
    DOCS --> DEV

    LAMBDA -.-> S3
    SQS -.-> LAMBDA
```

---

## Error Handling Flow

```mermaid
flowchart TD
    START[Start Processing] --> TRY{Try Operation}

    TRY -->|Success| PROCESS[Process Data]
    TRY -->|Failure| ERROR{Error Type?}

    ERROR -->|Network Error| RETRY[Retry with Backoff]
    ERROR -->|Validation Error| LOG_SKIP[Log & Skip Item]
    ERROR -->|Critical Error| HALT[Halt Processing]

    RETRY --> TRY
    LOG_SKIP --> CONTINUE[Continue to Next]
    HALT --> NOTIFY[Notify & Exit]

    PROCESS --> CONTINUE
    CONTINUE --> MORE{More Items?}
    MORE -->|Yes| TRY
    MORE -->|No| END[Complete]
```

---

## Summary

data-harvester follows these architectural principles:

1. **Modularity** - Each component handles a specific concern
2. **Extensibility** - Plugin architecture for custom functionality
3. **Scalability** - Parallel processing and cloud storage support
4. **Configurability** - Multiple configuration sources (INI, YAML, ENV)
5. **Observability** - Structured logging throughout the system
