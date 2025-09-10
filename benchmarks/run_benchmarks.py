#!/usr/bin/env python3
"""Run all benchmarks and generate report."""
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_benchmarks(output_json=True, verbose=True):
    """Run all benchmark tests."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    cmd = [
        sys.executable, "-m", "pytest",
        str(Path(__file__).parent),
        "--benchmark-only",
        "--benchmark-columns=mean,stddev,min,max,rounds",
        "--benchmark-sort=mean",
    ]

    if verbose:
        cmd.append("-v")

    if output_json:
        output_file = results_dir / f"benchmark_{timestamp}.json"
        cmd.append(f"--benchmark-json={output_file}")

    print("=" * 60)
    print("Data Harvester Benchmark Suite")
    print("=" * 60)
    print(f"Timestamp: {timestamp}")
    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)
    print()

    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)

    if output_json and result.returncode == 0:
        print()
        print(f"Results saved to: {output_file}")

    return result.returncode


def run_quick():
    """Run quick benchmarks for sanity check."""
    cmd = [
        sys.executable, "-m", "pytest",
        str(Path(__file__).parent / "bench_scrub.py"),
        "--benchmark-only",
        "-v",
        "--benchmark-disable-gc",
    ]

    print("Running quick benchmark (scrub module only)...")
    return subprocess.run(cmd, cwd=Path(__file__).parent.parent).returncode


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run data-harvester benchmarks")
    parser.add_argument("--quick", action="store_true", help="Run quick benchmarks only")
    parser.add_argument("--no-json", action="store_true", help="Skip JSON output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Less verbose output")

    args = parser.parse_args()

    if args.quick:
        return run_quick()
    else:
        return run_benchmarks(output_json=not args.no_json, verbose=not args.quiet)


if __name__ == "__main__":
    sys.exit(main())
