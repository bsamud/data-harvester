"""Benchmarks for the scrub (text cleaning) module."""
import pytest


class TestScrubBenchmarks:
    """Benchmark tests for text cleaning operations."""

    def test_normalize_short_text(self, benchmark, sample_short_text):
        """Benchmark normalize_text on short text."""
        from scrub.clean import normalize_text
        result = benchmark(normalize_text, sample_short_text)
        assert isinstance(result, str)

    def test_normalize_medium_text(self, benchmark, sample_medium_text):
        """Benchmark normalize_text on medium text."""
        from scrub.clean import normalize_text
        result = benchmark(normalize_text, sample_medium_text)
        assert isinstance(result, str)

    def test_normalize_long_text(self, benchmark, sample_long_text):
        """Benchmark normalize_text on long text."""
        from scrub.clean import normalize_text
        result = benchmark(normalize_text, sample_long_text)
        assert isinstance(result, str)

    def test_remove_html_tags(self, benchmark, sample_html_text):
        """Benchmark HTML tag removal."""
        from scrub.clean import remove_html_tags
        result = benchmark(remove_html_tags, sample_html_text)
        assert "<" not in result

    def test_batch_normalize(self, benchmark, sample_texts_batch):
        """Benchmark batch text normalization."""
        from scrub.clean import normalize_text

        def batch_normalize(texts):
            return [normalize_text(t) for t in texts]

        results = benchmark(batch_normalize, sample_texts_batch)
        assert len(results) == len(sample_texts_batch)
