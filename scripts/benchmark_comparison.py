#!/usr/bin/env python3
"""
Benchmark comparison between Rust and Python NIfTI statistics processors
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List


def run_rust_version(nifti_file: str, runs: int = 5) -> Dict:
    """Run the Rust version and measure performance."""
    #rust_binary = Path("./target/debug/nifti-stats")
    rust_binary = Path("./target/release/nifti-stats")

    if not rust_binary.exists():
        print("Error: Rust binary not found. Please build with 'cargo build --bin nifti-stats'")
        sys.exit(1)

    times = []
    result = None

    for i in range(runs):
        start = time.time()
        proc = subprocess.run(
            [str(rust_binary), nifti_file, "--output-format", "json"],
            capture_output=True,
            text=True
        )
        elapsed = (time.time() - start) * 1000  # Convert to ms

        if proc.returncode != 0:
            print(f"Error running Rust version: {proc.stderr}")
            sys.exit(1)

        times.append(elapsed)

        if i == 0:
            result = json.loads(proc.stdout)

    return {
        'times': times,
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'internal_time': result['processing_time_ms'] if result else 0,
        'result': result
    }


def run_python_version(nifti_file: str, runs: int = 5) -> Dict:
    """Run the Python version and measure performance."""
    python_script = Path("scripts/nifti_stats.py")

    if not python_script.exists():
        print("Error: Python script not found.")
        sys.exit(1)

    times = []
    result = None

    for i in range(runs):
        start = time.time()
        proc = subprocess.run(
            [sys.executable, str(python_script), nifti_file, "--output-format", "json"],
            capture_output=True,
            text=True
        )
        elapsed = (time.time() - start) * 1000  # Convert to ms

        if proc.returncode != 0:
            print(f"\nError running Python version:")
            print(f"STDERR: {proc.stderr}")
            print(f"STDOUT: {proc.stdout}")
            print("\nMake sure you have the required Python packages installed:")
            print("  pip install nibabel numpy")
            sys.exit(1)

        times.append(elapsed)

        if i == 0:
            try:
                result = json.loads(proc.stdout)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON output: {e}")
                print(f"Output was: {proc.stdout}")
                sys.exit(1)

    return {
        'times': times,
        'avg_time': sum(times) / len(times),
        'min_time': min(times),
        'max_time': max(times),
        'internal_time': result['processing_time_ms'] if result else 0,
        'result': result
    }


def compare_results(rust_result: Dict, python_result: Dict) -> None:
    """Compare the results from both implementations."""
    print("\n=== Result Comparison ===")

    # Check if unique values match
    rust_unique = rust_result['unique_values']
    python_unique = python_result['unique_values']

    if rust_unique == python_unique:
        print("✓ Unique values match")
    else:
        print("✗ Unique values differ")
        print(f"  Rust:   {len(rust_unique)} values")
        print(f"  Python: {len(python_unique)} values")

    # Compare statistics
    stats_to_compare = [
        'min_value', 'max_value', 'mean_value', 'std_value', 'variance',
        'total_unique_count'
    ]

    all_match = True
    for stat in stats_to_compare:
        rust_val = rust_result.get(stat, 0)
        python_val = python_result.get(stat, 0)

        # Allow small floating point differences
        if isinstance(rust_val, (int, float)) and isinstance(python_val, (int, float)):
            if abs(rust_val - python_val) < 1e-4:
                print(f"✓ {stat}: {rust_val:.4f}")
            else:
                print(f"✗ {stat} differs: Rust={rust_val:.4f}, Python={python_val:.4f}")
                all_match = False
        else:
            if rust_val == python_val:
                print(f"✓ {stat}: {rust_val}")
            else:
                print(f"✗ {stat} differs: Rust={rust_val}, Python={python_val}")
                all_match = False

    return all_match


def print_benchmark_results(rust_perf: Dict, python_perf: Dict) -> None:
    """Print benchmark results in a formatted table."""
    print("\n=== Performance Benchmark Results ===")
    print("\nExternal timing (includes process startup):")
    print(f"{'Metric':<20} {'Rust':<15} {'Python':<15} {'Speedup':<10}")
    print("-" * 60)

    speedup = python_perf['avg_time'] / rust_perf['avg_time']
    print(f"{'Average time':<20} {rust_perf['avg_time']:>10.2f} ms {python_perf['avg_time']:>10.2f} ms {speedup:>8.2f}x")

    speedup = python_perf['min_time'] / rust_perf['min_time']
    print(f"{'Min time':<20} {rust_perf['min_time']:>10.2f} ms {python_perf['min_time']:>10.2f} ms {speedup:>8.2f}x")

    speedup = python_perf['max_time'] / rust_perf['max_time']
    print(f"{'Max time':<20} {rust_perf['max_time']:>10.2f} ms {python_perf['max_time']:>10.2f} ms {speedup:>8.2f}x")

    print("\nInternal timing (pure processing, no startup):")
    speedup = python_perf['internal_time'] / rust_perf['internal_time']
    print(f"{'Processing time':<20} {rust_perf['internal_time']:>10.2f} ms {python_perf['internal_time']:>10.2f} ms {speedup:>8.2f}x")

    print("\nAll times (ms):")
    print(f"Rust:   {', '.join(f'{t:.2f}' for t in rust_perf['times'])}")
    print(f"Python: {', '.join(f'{t:.2f}' for t in python_perf['times'])}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python benchmark_comparison.py <nifti_file> [runs]")
        print("Example: python benchmark_comparison.py data/t1.nii 10")
        sys.exit(1)

    nifti_file = sys.argv[1]
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    if not Path(nifti_file).exists():
        print(f"Error: File '{nifti_file}' not found")
        sys.exit(1)

    print(f"Benchmarking NIfTI file: {nifti_file}")
    print(f"Number of runs: {runs}")
    print()

    print("Running Rust version...")
    rust_perf = run_rust_version(nifti_file, runs)

    print("Running Python version...")
    python_perf = run_python_version(nifti_file, runs)

    # Compare results for correctness
    results_match = compare_results(rust_perf['result'], python_perf['result'])

    # Print performance comparison
    print_benchmark_results(rust_perf, python_perf)

    # Summary
    print("\n=== Summary ===")
    if results_match:
        print("✓ Results are consistent between implementations")
    else:
        print("✗ Warning: Results differ between implementations")

    # Overall performance (external timing)
    overall_speedup = python_perf['avg_time'] / rust_perf['avg_time']
    print(f"\nOverall performance (including startup):")
    if overall_speedup > 1.0:
        print(f"  ✓ Rust is {overall_speedup:.2f}x faster than Python")
    else:
        print(f"  ✗ Python is {1/overall_speedup:.2f}x faster than Rust")

    # Internal processing performance
    internal_speedup = python_perf['internal_time'] / rust_perf['internal_time']
    print(f"\nInternal processing only:")
    if internal_speedup > 1.0:
        print(f"  ✓ Rust is {internal_speedup:.2f}x faster than Python")
    else:
        print(f"  ✗ Python is {1/internal_speedup:.2f}x faster than Rust")
        print(f"     (NumPy's optimized C code gives Python an edge here)")

    # Recommendation
    print(f"\nRecommendation:")
    if overall_speedup > 1.0:
        print(f"  Use Rust for better overall performance ({overall_speedup:.2f}x faster)")
        if internal_speedup < 1.0:
            print(f"  Note: Try 'cargo build --release' for even better performance")
    else:
        print(f"  Python is faster overall for this use case")


if __name__ == '__main__':
    main()
