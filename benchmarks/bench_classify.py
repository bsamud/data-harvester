"""Benchmarks for the classify (ML) module."""
import pytest


class TestClassifyBenchmarks:
    """Benchmark tests for document classification operations."""

    @pytest.fixture(scope="class")
    def trained_classifier(self, training_data):
        """Create and train classifier once per class."""
        from classify.classify import DocumentClassifier
        texts, labels = training_data
        classifier = DocumentClassifier()
        classifier.train(texts, labels)
        return classifier

    def test_train_classifier(self, benchmark, training_data):
        """Benchmark classifier training."""
        from classify.classify import DocumentClassifier
        texts, labels = training_data

        def train_new():
            classifier = DocumentClassifier()
            classifier.train(texts, labels)
            return classifier

        result = benchmark(train_new)
        assert result.is_trained

    def test_predict_single(self, benchmark, trained_classifier):
        """Benchmark single document prediction."""
        text = ["New technology announcement from major company"]
        result = benchmark(trained_classifier.predict, text)
        assert len(result) == 1

    def test_predict_batch_small(self, benchmark, trained_classifier):
        """Benchmark batch prediction (10 docs)."""
        texts = ["Document about technology and innovation"] * 10
        result = benchmark(trained_classifier.predict, texts)
        assert len(result) == 10

    def test_predict_batch_medium(self, benchmark, trained_classifier):
        """Benchmark batch prediction (100 docs)."""
        texts = ["Document about technology and innovation"] * 100
        result = benchmark(trained_classifier.predict, texts)
        assert len(result) == 100

    def test_predict_batch_large(self, benchmark, trained_classifier):
        """Benchmark batch prediction (500 docs)."""
        texts = ["Document about technology and innovation"] * 500
        result = benchmark(trained_classifier.predict, texts)
        assert len(result) == 500

    def test_create_pipeline(self, benchmark):
        """Benchmark pipeline creation."""
        from classify.classify import DocumentClassifier
        classifier = DocumentClassifier()
        result = benchmark(classifier.create_pipeline)
        assert result is not None
