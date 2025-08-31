#!/usr/bin/env python3
"""
NIfTI File Processor - Python version using nibabel and numpy.

This script processes NIfTI files and computes statistical information,
equivalent to the Rust version for performance comparison.
"""

import sys
import os
import time
import numpy as np
import nibabel as nib
from pathlib import Path


def main():
    """
    Main function to process NIfTI files and display metadata and statistics.
    
    Returns
    -------
    None
    """
    print("=== NIfTI File Processor (Python) ===")
    
    # Get file path from command line arguments or use default
    file_path = sys.argv[1] if len(sys.argv) > 1 else "data/avg152T1.nii"
    
    # Check if file exists
    if not Path(file_path).exists():
        print(f"Warning: File '{file_path}' not found. Please provide a valid NIfTI file.")
        print("Usage: python nifti_processor.py [path/to/file.nii]")
        return
    
    try:
        # Start timing for file loading
        start_time = time.perf_counter()
        
        # Load the NIfTI file
        nii_obj = nib.load(file_path)
        header = nii_obj.header
        
        load_time = time.perf_counter() - start_time
        
        # Print basic file information
        print(f"NIfTI File: {file_path}")
        print("----------------------------------------")
        
        # Print dimensions
        dims = header.get_data_shape()
        print(f"Dimensions: {dims}")
        if len(dims) >= 3:
            print(f"Dimensions: {dims[0]} x {dims[1]} x {dims[2]}")
        
        # Print data type
        data_type = header.get_data_dtype()
        print(f"Data type: {data_type}")
        
        # Print voxel dimensions
        pixdim = header.get_zooms()
        if len(pixdim) >= 3:
            print(f"Voxel dimensions: {pixdim[:3]} mm")
        
        # Print other metadata
        print(f"Intent: {header.get_intent()[0]}")
        print(f"Slice order: {header.get('slice_code', 'unknown')}")
        print(f"Slice end: {header.get('slice_end', 'unknown')}")
        print(f"Units: spatial={header.get_xyzt_units()[0]}, temporal={header.get_xyzt_units()[1]}")
        print(f"Slope: {header.get('scl_slope', 1.0)}")
        print(f"Intercept: {header.get('scl_inter', 0.0)}")
        print(f"Endianness: {header.endianness}")
        
        # Additional information
        print(f"Calibration: ({header.get('cal_min', 0)}, {header.get('cal_max', 0)})")
        print(f"Voxel offset: {header.get('vox_offset', 0)}")
        
        # Load volume data and convert to float32
        print("\nLoading volume data...")
        volume_start_time = time.perf_counter()
        
        # Get data as numpy array and convert to float32
        volume = nii_obj.get_fdata(dtype=np.float32)
        
        volume_load_time = time.perf_counter() - volume_start_time
        
        print(f"Volume shape: {volume.shape}")
        print(f"First voxel value: {volume.flat[0]}")
        
        # Compute statistics with timing
        stats_start_time = time.perf_counter()
        
        # Filter out non-finite values for robust statistics
        finite_mask = np.isfinite(volume)
        finite_volume = volume[finite_mask]
        
        if len(finite_volume) == 0:
            print("Warning: No finite values found in volume!")
            return
            
        # Compute statistics using numpy (similar to NumPy)
        min_val = np.min(finite_volume)
        max_val = np.max(finite_volume)
        mean_val = np.mean(finite_volume)
        std_val = np.std(finite_volume, ddof=0)  # ddof=0 like NumPy default
        var_val = np.var(finite_volume, ddof=0)
        
        stats_time = time.perf_counter() - stats_start_time
        
        print(f"Min voxel value: {min_val}")
        print(f"Max voxel value: {max_val}")
        print(f"Mean voxel value: {mean_val}")
        print(f"Standard deviation: {std_val}")
        print(f"Variance: {var_val}")
        
        # Data type specific information
        dtype_info = {
            np.uint8: "8-bit unsigned integer",
            np.int16: "16-bit signed integer", 
            np.int32: "32-bit signed integer",
            np.float32: "32-bit floating point",
            np.float64: "64-bit floating point"
        }
        
        dtype_desc = dtype_info.get(data_type.type, "Other")
        print(f"Data type: {dtype_desc}")
        
        # Performance timing results
        total_time = time.perf_counter() - start_time
        print("\n----------------------------------------")
        print("Performance Timing:")
        print(f"File loading time: {load_time:.4f} seconds")
        print(f"Volume data loading: {volume_load_time:.4f} seconds") 
        print(f"Statistics computation: {stats_time:.4f} seconds")
        print(f"Total execution time: {total_time:.4f} seconds")
        print("----------------------------------------")
        print("Successfully read NIfTI file and displayed metadata.")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return


def benchmark_statistics(volume, iterations=10):
    """
    Benchmark different approaches for computing statistics.
    
    Parameters
    ----------
    volume : numpy.ndarray
        The volume data to compute statistics on
    iterations : int, default=10
        Number of iterations for benchmarking
        
    Returns
    -------
    dict
        Dictionary containing timing results for different methods
    """
    print(f"\nBenchmarking statistics computation ({iterations} iterations)...")
    
    # Filter finite values once
    finite_mask = np.isfinite(volume)
    finite_volume = volume[finite_mask]
    
    methods = {}
    
    # Method 1: Standard numpy functions
    start_time = time.perf_counter()
    for _ in range(iterations):
        min_val = np.min(finite_volume)
        max_val = np.max(finite_volume) 
        mean_val = np.mean(finite_volume)
        std_val = np.std(finite_volume, ddof=0)
    methods['numpy_separate'] = (time.perf_counter() - start_time) / iterations
    
    # Method 2: Single pass with manual computation
    start_time = time.perf_counter()
    for _ in range(iterations):
        min_val = np.min(finite_volume)
        max_val = np.max(finite_volume)
        sum_val = np.sum(finite_volume)
        sum_sq = np.sum(finite_volume ** 2)
        n = len(finite_volume)
        mean_val = sum_val / n
        var_val = (sum_sq - sum_val * mean_val) / n
        std_val = np.sqrt(var_val)
    methods['numpy_optimized'] = (time.perf_counter() - start_time) / iterations
    
    # Method 3: Using numpy statistical functions together
    start_time = time.perf_counter() 
    for _ in range(iterations):
        stats = {
            'min': np.min(finite_volume),
            'max': np.max(finite_volume),
            'mean': np.mean(finite_volume),
            'std': np.std(finite_volume, ddof=0)
        }
    methods['numpy_dict'] = (time.perf_counter() - start_time) / iterations
    
    return methods


if __name__ == "__main__":
    main()