"""Document classification using scikit-learn"""
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
