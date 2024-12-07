"""Training pipeline for classification models"""
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

        log.info("
Classification Report:")
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
