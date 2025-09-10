"""Benchmarks for the parallel processing module."""
import pytest
import time


def cpu_bound_task(x):
    """Simulate CPU-bound work."""
    total = 0
    for i in range(10000):
        total += i * x
    return total


def io_bound_task(x):
    """Simulate I/O-bound work."""
    time.sleep(0.01)
    return x * 2


class TestParallelBenchmarks:
    """Benchmark tests for parallel processing operations."""

    def test_sequential_baseline(self, benchmark):
        """Baseline: sequential processing."""
        items = list(range(50))

        def sequential():
            return [cpu_bound_task(i) for i in items]

        result = benchmark(sequential)
        assert len(result) == 50

    def test_parallel_2_workers(self, benchmark):
        """Benchmark with 2 workers."""
        from common.parallel_processor import ParallelProcessor
        processor = ParallelProcessor(num_workers=2)
        items = list(range(50))
        result = benchmark(processor.process_batch, cpu_bound_task, items)
        assert len(result) == 50

    def test_parallel_4_workers(self, benchmark):
        """Benchmark with 4 workers."""
        from common.parallel_processor import ParallelProcessor
        processor = ParallelProcessor(num_workers=4)
        items = list(range(50))
        result = benchmark(processor.process_batch, cpu_bound_task, items)
        assert len(result) == 50

    def test_parallel_8_workers(self, benchmark):
        """Benchmark with 8 workers (M3 performance cores)."""
        from common.parallel_processor import ParallelProcessor
        processor = ParallelProcessor(num_workers=8)
        items = list(range(50))
        result = benchmark(processor.process_batch, cpu_bound_task, items)
        assert len(result) == 50

    def test_parallel_auto_workers(self, benchmark):
        """Benchmark with auto-detected worker count."""
        from common.parallel_processor import ParallelProcessor
        processor = ParallelProcessor()  # Uses cpu_count
        items = list(range(50))
        result = benchmark(processor.process_batch, cpu_bound_task, items)
        assert len(result) == 50

    def test_scaling_comparison(self):
        """Compare scaling across worker counts (not a benchmark, just report)."""
        from common.parallel_processor import ParallelProcessor
        import time

        items = list(range(100))
        results = {}

        for workers in [1, 2, 4, 8]:
            processor = ParallelProcessor(num_workers=workers)
            start = time.perf_counter()
            processor.process_batch(cpu_bound_task, items)
            elapsed = time.perf_counter() - start
            results[workers] = elapsed

        print("\nScaling Results:")
        baseline = results[1]
        for workers, elapsed in results.items():
            speedup = baseline / elapsed
            print(f"  {workers} workers: {elapsed:.3f}s (speedup: {speedup:.2f}x)")
