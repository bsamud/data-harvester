"""Named Entity Recognition using spaCy"""
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
