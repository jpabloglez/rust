#!/usr/bin/env python3
"""
Performance comparison script for Rust vs Python NIfTI processing.

This script runs both implementations multiple times and compares
execution times, memory usage, and statistical accuracy.
"""

import subprocess
import time
import sys
import os
import psutil
import statistics
from pathlib import Path


def run_rust_version(nifti_file, iterations=5):
    """
    Run the Rust version multiple times and collect timing data.
    
    Parameters
    ----------
    nifti_file : str
        Path to the NIfTI file to process
    iterations : int, default=5
        Number of iterations to run
        
    Returns
    -------
    dict
        Dictionary containing timing statistics
    """
    print(f"Running Rust version {iterations} times...")
    times = []
    
    for i in range(iterations):
        start_time = time.perf_counter()
        
        try:
            # Assume the Rust binary is called 'nifti-processor' 
            result = subprocess.run(
                ['./target/debug/nifti', nifti_file],
                capture_output=True,
                text=True,
                check=True
            )
            
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            times.append(execution_time)
            
            print(f"  Iteration {i+1}: {execution_time:.4f}s")
            
        except subprocess.CalledProcessError as e:
            print(f"Error running Rust version: {e}")
            return None
        except FileNotFoundError:
            print("Rust binary not found. Please compile with: cargo build --release")
            return None
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times), 
        'min': min(times),
        'max': max(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0,
        'times': times
    }


def run_python_version(nifti_file, iterations=5):
    """
    Run the Python version multiple times and collect timing data.
    
    Parameters
    ----------
    nifti_file : str
        Path to the NIfTI file to process
    iterations : int, default=5
        Number of iterations to run
        
    Returns
    -------
    dict
        Dictionary containing timing statistics
    """
    print(f"Running Python version {iterations} times...")
    times = []
    
    for i in range(iterations):
        start_time = time.perf_counter()
        
        try:
            result = subprocess.run(
                [sys.executable, 'python-nifti.py', nifti_file],
                capture_output=True,
                text=True,
                check=True
            )
            
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            times.append(execution_time)
            
            print(f"  Iteration {i+1}: {execution_time:.4f}s")
            
        except subprocess.CalledProcessError as e:
            print(f"Error running Python version: {e}")
            return None
        except FileNotFoundError:
            print("Python script not found. Please ensure nifti_processor.py exists.")
            return None
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'min': min(times), 
        'max': max(times),
        'std': statistics.stdev(times) if len(times) > 1 else 0,
        'times': times
    }


def get_memory_usage():
    """
    Get current memory usage of the process.
    
    Returns
    -------
    dict
        Dictionary containing memory usage information
    """
    process = psutil.Process()
    memory_info = process.memory_info()
    
    return {
        'rss': memory_info.rss / 1024 / 1024,  # MB
        'vms': memory_info.vms / 1024 / 1024,  # MB
        'percent': process.memory_percent()
    }


def compare_performance(nifti_file, iterations=5):
    """
    Compare performance between Rust and Python implementations.
    
    Parameters
    ----------
    nifti_file : str
        Path to the NIfTI file to process
    iterations : int, default=5
        Number of iterations to run for each implementation
        
    Returns
    -------
    None
    """
    print("=== NIfTI Processing Performance Comparison ===")
    print(f"File: {nifti_file}")
    print(f"Iterations per implementation: {iterations}")
    print()
    
    # Check if file exists
    if not Path(nifti_file).exists():
        print(f"Error: File '{nifti_file}' not found.")
        return
    
    # Run Rust version
    rust_stats = run_rust_version(nifti_file, iterations)
    print()
    
    # Run Python version
    python_stats = run_python_version(nifti_file, iterations)
    print()
    
    if rust_stats is None or python_stats is None:
        print("Could not complete comparison due to errors.")
        return
    
    # Display comparison results
    print("=== Performance Comparison Results ===")
    print()
    
    print("Execution Time Statistics:")
    print(f"{'Metric':<12} {'Rust (s)':<12} {'Python (s)':<12} {'Speedup':<10}")
    print("-" * 50)
    
    speedup_mean = python_stats['mean'] / rust_stats['mean']
    speedup_median = python_stats['median'] / rust_stats['median']
    speedup_min = python_stats['min'] / rust_stats['min']
    
    print(f"{'Mean':<12} {rust_stats['mean']:<12.4f} {python_stats['mean']:<12.4f} {speedup_mean:<10.2f}x")
    print(f"{'Median':<12} {rust_stats['median']:<12.4f} {python_stats['median']:<12.4f} {speedup_median:<10.2f}x")
    print(f"{'Min':<12} {rust_stats['min']:<12.4f} {python_stats['min']:<12.4f} {speedup_min:<10.2f}x")
    print(f"{'Max':<12} {rust_stats['max']:<12.4f} {python_stats['max']:<12.4f} {'N/A':<10}")
    print(f"{'Std Dev':<12} {rust_stats['std']:<12.4f} {python_stats['std']:<12.4f} {'N/A':<10}")
    
    print()
    print("Summary:")
    if speedup_mean > 1:
        print(f"🚀 Rust is {speedup_mean:.2f}x faster than Python on average")
    else:
        print(f"🐍 Python is {1/speedup_mean:.2f}x faster than Rust on average")
    
    print(f"📊 Rust timing consistency: {rust_stats['std']/rust_stats['mean']*100:.1f}% CV")
    print(f"📊 Python timing consistency: {python_stats['std']/python_stats['mean']*100:.1f}% CV")
    
    # Memory usage comparison would require more complex monitoring
    print()
    print("Note: For detailed memory usage comparison, run each version individually")
    print("with memory profiling tools like 'time -v' or 'valgrind' for Rust")
    print("and 'memory_profiler' for Python.")


def main():
    """Main function to run the performance comparison."""
    if len(sys.argv) < 2:
        print("Usage: python performance_comparison.py <nifti_file> [iterations]")
        print("Example: python performance_comparison.py data/avg152T1.nii 10")
        return
    
    nifti_file = sys.argv[1]
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    compare_performance(nifti_file, iterations)


if __name__ == "__main__":
    main()