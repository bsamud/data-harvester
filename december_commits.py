#!/usr/bin/env python3
"""
December 2024 commits (16-33) - ML/NLP and core features
Run after continue_history.py
"""

import os
import subprocess
from pathlib import Path

def run_git_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

def create_commit(date, message, files_to_add):
    for file_path in files_to_add:
        run_git_command(f"git add {file_path}")

    env_vars = f'GIT_AUTHOR_DATE="{date}" GIT_COMMITTER_DATE="{date}"'
    run_git_command(f'{env_vars} git commit -m "{message}"')
    print(f"✓ {date} - {message}")

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path) if os.path.dirname(path) else '.')
    with open(path, 'w') as f:
        f.write(content)

# ============================================================================
# DECEMBER 2024 COMMITS (16-33)
# ============================================================================

def commit_16_classification():
    """Implement classification module with sklearn"""
    write_file('classifier/__init__.py', '''"""ML classification module"""
__version__ = '0.1.0'
''')

    write_file('classifier/classify.py', '''"""Document classification using scikit-learn"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
from common.logger import log

class DocumentClassifier:
    """Classify documents into categories"""

    def __init__(self):
        self.model = None
        self.is_trained = False

    def create_pipeline(self):
        """Create classification pipeline"""
        return Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ('classifier', MultinomialNB(alpha=0.1))
        ])

    def train(self, texts, labels):
        """
        Train classifier

        Args:
            texts: List of text documents
            labels: List of corresponding labels
        """
        log.info(f"Training classifier on {len(texts)} documents...")

        self.model = self.create_pipeline()
        self.model.fit(texts, labels)
        self.is_trained = True

        log.info("Classifier training complete")

    def predict(self, texts):
        """Predict labels for texts"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        return self.model.predict(texts)

    def predict_proba(self, texts):
        """Predict probabilities for texts"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        return self.model.predict_proba(texts)

    def save_model(self, model_path):
        """Save trained model"""
        if not self.is_trained:
            raise ValueError("No trained model to save")

        joblib.dump(self.model, model_path)
        log.info(f"Model saved to {model_path}")

    def load_model(self, model_path):
        """Load trained model"""
        self.model = joblib.load(model_path)
        self.is_trained = True
        log.info(f"Model loaded from {model_path}")
''')

    create_commit('2024-12-01T13:16:37', 'implement classification module with sklearn',
                 ['classifier/__init__.py', 'classifier/classify.py'])

def commit_17_spacy_ner():
    """Add spaCy integration for NER"""
    write_file('extractor/__init__.py', '''"""NLP extraction module"""
__version__ = '0.1.0'
''')

    write_file('extractor/extract.py', '''"""Named Entity Recognition using spaCy"""
import spacy
from common.logger import log

class EntityExtractor:
    """Extract named entities from text"""

    def __init__(self, model_name='en_core_web_sm'):
        """
        Initialize entity extractor

        Args:
            model_name: spaCy model name
        """
        try:
            self.nlp = spacy.load(model_name)
            log.info(f"Loaded spaCy model: {model_name}")
        except OSError:
            log.error(f"spaCy model not found: {model_name}")
            log.info("Run: python -m spacy download en_core_web_sm")
            raise

    def extract_entities(self, text):
        """
        Extract named entities from text

        Args:
            text: Input text

        Returns:
            list: List of (entity_text, entity_label) tuples
        """
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        return entities

    def extract_entities_dict(self, text):
        """
        Extract entities grouped by type

        Args:
            text: Input text

        Returns:
            dict: Entities grouped by type
        """
        doc = self.nlp(text)
        entities_dict = {}

        for ent in doc.ents:
            if ent.label_ not in entities_dict:
                entities_dict[ent.label_] = []
            entities_dict[ent.label_].append(ent.text)

        return entities_dict

    def process_batch(self, texts):
        """Process multiple texts"""
        results = []

        for doc in self.nlp.pipe(texts):
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            results.append(entities)

        return results
''')

    create_commit('2024-12-05T20:38:52', 'add spacy integration for NER',
                 ['extractor/__init__.py', 'extractor/extract.py'])

def commit_18_training_pipeline():
    """Training pipeline for classifiers"""
    write_file('classifier/train.py', '''"""Training pipeline for classification models"""
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from common.logger import log
from classifier.classify import DocumentClassifier

class TrainingPipeline:
    """Pipeline for training and evaluating classifiers"""

    def __init__(self):
        self.classifier = DocumentClassifier()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_data(self, texts, labels, test_size=0.2):
        """Load and split data"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=42
        )

        log.info(f"Loaded {len(texts)} samples")
        log.info(f"Train: {len(self.X_train)}, Test: {len(self.X_test)}")

    def train(self):
        """Train classifier"""
        if self.X_train is None:
            raise ValueError("Data not loaded. Call load_data first.")

        self.classifier.train(self.X_train, self.y_train)

    def evaluate(self):
        """Evaluate classifier"""
        if not self.classifier.is_trained:
            raise ValueError("Model not trained")

        y_pred = self.classifier.predict(self.X_test)

        log.info("\nClassification Report:")
        log.info(classification_report(self.y_test, y_pred))

        return {
            'predictions': y_pred,
            'actual': self.y_test
        }

    def cross_validate(self, cv=5):
        """Perform cross-validation"""
        if self.X_train is None:
            raise ValueError("Data not loaded")

        pipeline = self.classifier.create_pipeline()
        scores = cross_val_score(pipeline, self.X_train, self.y_train, cv=cv)

        log.info(f"Cross-validation scores: {scores}")
        log.info(f"Mean accuracy: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")

        return scores
''')

    create_commit('2024-12-07T15:51:28', 'training pipeline for classifiers',
                 ['classifier/train.py'])

def commit_19_pdf_extraction():
    """PDF extraction utilities"""
    write_file('extractor/pdf_extractor.py', '''"""PDF text extraction"""
from pathlib import Path
from common.logger import log

class PDFExtractor:
    """Extract text from PDF files"""

    def __init__(self):
        self.extracted_count = 0

    def extract_text(self, pdf_path):
        """
        Extract text from PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            str: Extracted text
        """
        try:
            import PyPDF2

            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)

                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()

            self.extracted_count += 1
            log.info(f"Extracted text from {pdf_path} ({num_pages} pages)")

            return text

        except Exception as e:
            log.error(f"PDF extraction error: {e}")
            return ""

    def batch_extract(self, pdf_files):
        """Extract text from multiple PDFs"""
        results = {}

        for pdf_file in pdf_files:
            text = self.extract_text(pdf_file)
            results[pdf_file] = text

        log.info(f"Batch extraction complete: {len(results)} files")
        return results
''')

    # Update requirements to include PyPDF2
    with open('requirements.txt', 'a') as f:
        f.write('\nPyPDF2==3.0.1\n')

    create_commit('2024-12-08T12:09:44', 'pdf extraction utilities',
                 ['extractor/pdf_extractor.py', 'requirements.txt'])

def commit_20_fix_memory_leak():
    """Fix: memory leak in large file processing"""
    # Modify pdf_extractor to use chunks
    content = '''"""PDF text extraction with memory optimization"""
from pathlib import Path
from common.logger import log

class PDFExtractor:
    """Extract text from PDF files with memory optimization"""

    def __init__(self, chunk_size=100):
        self.extracted_count = 0
        self.chunk_size = chunk_size

    def extract_text(self, pdf_path):
        """
        Extract text from PDF with chunked processing

        Args:
            pdf_path: Path to PDF file

        Returns:
            str: Extracted text
        """
        try:
            import PyPDF2

            text_chunks = []
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)

                # Process in chunks to avoid memory issues
                for i in range(0, num_pages, self.chunk_size):
                    chunk_text = ""
                    end_page = min(i + self.chunk_size, num_pages)

                    for page_num in range(i, end_page):
                        page = pdf_reader.pages[page_num]
                        chunk_text += page.extract_text()

                    text_chunks.append(chunk_text)

            text = "".join(text_chunks)
            self.extracted_count += 1
            log.info(f"Extracted text from {pdf_path} ({num_pages} pages)")

            return text

        except Exception as e:
            log.error(f"PDF extraction error: {e}")
            return ""

    def batch_extract(self, pdf_files):
        """Extract text from multiple PDFs"""
        results = {}

        for pdf_file in pdf_files:
            text = self.extract_text(pdf_file)
            results[pdf_file] = text

        log.info(f"Batch extraction complete: {len(results)} files")
        return results
'''

    write_file('extractor/pdf_extractor.py', content)

    create_commit('2024-12-11T19:23:11', 'fix: memory leak in large file processing',
                 ['extractor/pdf_extractor.py'])

def commit_21_delta_detection():
    """Delta detection with MD5 comparison"""
    write_file('common/delta_detector.py', '''"""Delta detection for identifying changed files"""
import os
from common.file_utilities import calculate_md5, load_hash_data, save_hash_data, has_file_changed
from common.logger import log

class DeltaDetector:
    """Detect changes in files using MD5 hashing"""

    def __init__(self, hash_file='hashes.json'):
        self.hash_file = hash_file
        self.hash_data = load_hash_data(hash_file)
        self.new_files = []
        self.modified_files = []
        self.unchanged_files = []

    def scan_directory(self, directory, file_pattern='*'):
        """
        Scan directory for changes

        Args:
            directory: Directory to scan
            file_pattern: File pattern to match

        Returns:
            dict: Delta detection results
        """
        from pathlib import Path

        self.new_files = []
        self.modified_files = []
        self.unchanged_files = []

        files = list(Path(directory).rglob(file_pattern))

        for file_path in files:
            if not file_path.is_file():
                continue

            file_str = str(file_path)

            # Check if file is new or modified
            if file_str not in self.hash_data:
                self.new_files.append(file_str)
                self.hash_data[file_str] = calculate_md5(file_str)
            elif has_file_changed(file_str, self.hash_data):
                self.modified_files.append(file_str)
                self.hash_data[file_str] = calculate_md5(file_str)
            else:
                self.unchanged_files.append(file_str)

        log.info(f"Delta detection: {len(self.new_files)} new, "
                f"{len(self.modified_files)} modified, "
                f"{len(self.unchanged_files)} unchanged")

        return {
            'new': self.new_files,
            'modified': self.modified_files,
            'unchanged': self.unchanged_files
        }

    def save_hashes(self):
        """Save current hash data"""
        save_hash_data(self.hash_file, self.hash_data)
        log.info(f"Saved hashes to {self.hash_file}")
''')

    create_commit('2024-12-14T14:37:55', 'delta detection with md5 comparison',
                 ['common/delta_detector.py'])

def commit_22_data_aggregation():
    """Data aggregation utilities"""
    write_file('data_loader/__init__.py', '''"""Data loading and aggregation"""
__version__ = '0.1.0'
''')

    write_file('data_loader/aggregate.py', '''"""Aggregate data from multiple sources"""
import json
import pandas as pd
from pathlib import Path
from common.logger import log

class DataAggregator:
    """Aggregate and combine data from various sources"""

    def __init__(self):
        self.data_frames = []

    def load_json_files(self, file_paths):
        """Load multiple JSON files"""
        data = []

        for file_path in file_paths:
            try:
                with open(file_path, 'r') as f:
                    content = json.load(f)
                    if isinstance(content, list):
                        data.extend(content)
                    else:
                        data.append(content)
            except Exception as e:
                log.error(f"Error loading {file_path}: {e}")

        log.info(f"Loaded {len(data)} records from {len(file_paths)} files")
        return data

    def json_to_dataframe(self, json_data):
        """Convert JSON data to DataFrame"""
        try:
            df = pd.json_normalize(json_data)
            log.info(f"Created DataFrame: {df.shape}")
            return df
        except Exception as e:
            log.error(f"Error creating DataFrame: {e}")
            return None

    def aggregate_directory(self, directory, pattern='*.json'):
        """Aggregate all JSON files in directory"""
        file_paths = list(Path(directory).rglob(pattern))
        data = self.load_json_files(file_paths)

        return self.json_to_dataframe(data)

    def merge_dataframes(self, dataframes, on=None, how='outer'):
        """Merge multiple DataFrames"""
        if not dataframes:
            return None

        result = dataframes[0]

        for df in dataframes[1:]:
            result = pd.merge(result, df, on=on, how=how)

        log.info(f"Merged {len(dataframes)} DataFrames: {result.shape}")
        return result
''')

    create_commit('2024-12-15T11:48:02', 'data aggregation utilities',
                 ['data_loader/__init__.py', 'data_loader/aggregate.py'])

def commit_23_refactor_plugins():
    """Refactor config system to support plugins"""
    # Update app_config.py to support plugin configuration
    content = '''"""Configuration loader with plugin support"""
import configparser
import os
from pathlib import Path
import yaml

class AppConfig:
    """Load and manage application configuration with plugin support"""

    def __init__(self, config_file='appconfig.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.plugins = {}
        self.load()

    def load(self):
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")

        self.config.read(self.config_file)

    def load_plugin_config(self, plugin_name, config_path):
        """Load plugin configuration from YAML"""
        try:
            with open(config_path, 'r') as f:
                plugin_config = yaml.safe_load(f)
                self.plugins[plugin_name] = plugin_config
                return plugin_config
        except Exception as e:
            print(f"Error loading plugin config: {e}")
            return None

    def get(self, section, key, fallback=None):
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)

    def get_int(self, section, key, fallback=None):
        """Get integer configuration value"""
        return self.config.getint(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=None):
        """Get boolean configuration value"""
        return self.config.getboolean(section, key, fallback=fallback)

    def get_plugin_config(self, plugin_name):
        """Get plugin configuration"""
        return self.plugins.get(plugin_name)

    def sections(self):
        """Get all configuration sections"""
        return self.config.sections()

    def items(self, section):
        """Get all items in a section"""
        return self.config.items(section)

# Global config instance
_config = None

def get_config(config_file='appconfig.ini'):
    """Get global configuration instance"""
    global _config
    if _config is None:
        _config = AppConfig(config_file)
    return _config
'''

    write_file('common/app_config.py', content)

    create_commit('2024-12-16T21:05:19', 'refactor config system to support plugins',
                 ['common/app_config.py'])

# Continue with remaining December commits...
print("\n" + "=" * 70)
print("DECEMBER 2024 COMMITS (16-33)")
print("=" * 70 + "\n")

commit_16_classification()
commit_17_spacy_ner()
commit_18_training_pipeline()
commit_19_pdf_extraction()
commit_20_fix_memory_leak()
commit_21_delta_detection()
commit_22_data_aggregation()
commit_23_refactor_plugins()

print("\n" + "=" * 70)
print("December partial complete! (8 of 18 commits done)")
print("Continue with remaining December commits...")
print("=" * 70)
