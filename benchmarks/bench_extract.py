"""Benchmarks for the extract (NLP) module."""
import pytest


class TestExtractBenchmarks:
    """Benchmark tests for entity extraction operations."""

    @pytest.fixture(scope="class")
    def extractor(self):
        """Create extractor instance once per class."""
        from extract.extract import EntityExtractor
        return EntityExtractor()

    def test_extract_short_text(self, benchmark, extractor, sample_short_text):
        """Benchmark entity extraction on short text."""
        result = benchmark(extractor.extract_entities, sample_short_text)
        assert isinstance(result, list)

    def test_extract_medium_text(self, benchmark, extractor, sample_medium_text):
        """Benchmark entity extraction on medium text."""
        result = benchmark(extractor.extract_entities, sample_medium_text)
        assert isinstance(result, list)

    def test_extract_long_text(self, benchmark, extractor, sample_long_text):
        """Benchmark entity extraction on long text."""
        result = benchmark(extractor.extract_entities, sample_long_text)
        assert isinstance(result, list)

    def test_batch_extraction(self, benchmark, extractor, sample_texts_batch):
        """Benchmark batch entity extraction."""
        result = benchmark(extractor.process_batch, sample_texts_batch)
        assert len(result) == len(sample_texts_batch)

    def test_extract_from_seed_articles(self, benchmark, extractor, seed_articles):
        """Benchmark extraction on real seed data."""
        if not seed_articles:
            pytest.skip("Seed articles not available")

        texts = [a["content"] for a in seed_articles[:5]]

        def extract_all():
            return [extractor.extract_entities(t) for t in texts]

        result = benchmark(extract_all)
        assert len(result) == len(texts)
