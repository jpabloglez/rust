#!/usr/bin/env python3
"""
NIfTI Statistics Processor - Python version
Replicates the Rust nifti-stats functionality for performance comparison
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import nibabel as nib
import numpy as np


def process_nifti_file(file_path: str) -> Dict:
    """Process a NIfTI file and extract statistics."""
    start_time = time.time()

    # Load the NIfTI file
    nii = nib.load(file_path)
    header = nii.header

    # Extract basic information
    dimensions = list(header.get_data_shape())
    voxel_dimensions = header.get_zooms()[:3] if len(header.get_zooms()) >= 3 else []
    data_type = str(header.get_data_dtype())

    # Extract header values - ensure native Python types for JSON serialization
    calibration_min = float(header['cal_min'].item()) if 'cal_min' in header else 0.0
    calibration_max = float(header['cal_max'].item()) if 'cal_max' in header else 0.0
    voxel_offset = float(header['vox_offset'].item()) if 'vox_offset' in header else 0.0
    slope = float(header['scl_slope'].item()) if 'scl_slope' in header else 1.0
    intercept = float(header['scl_inter'].item()) if 'scl_inter' in header else 0.0

    # Get volume data as float32
    volume = nii.get_fdata(dtype=np.float32)
    volume_shape = list(volume.shape)

    # Compute statistics
    first_voxel = float(volume.flat[0])

    # Filter out NaN and Inf values for statistics
    valid_data = volume[np.isfinite(volume)]

    if len(valid_data) > 0:
        min_value = float(np.min(valid_data))
        max_value = float(np.max(valid_data))
        mean_value = float(np.mean(valid_data))
        std_value = float(np.std(valid_data))
        variance = float(np.var(valid_data))
    else:
        min_value = max_value = mean_value = std_value = variance = float('nan')

    # Extract unique values with early exit optimization
    # Only collect unique values if there are fewer than 200 different values
    MAX_UNIQUE_THRESHOLD = 200
    MAX_DISPLAY_VALUES = 100

    unique_values, total_unique_count, unique_values_truncated = extract_unique_values(
        volume, MAX_UNIQUE_THRESHOLD, MAX_DISPLAY_VALUES
    )

    processing_time = (time.time() - start_time) * 1000.0  # Convert to milliseconds

    return {
        'file_path': file_path,
        'dimensions': dimensions,
        'voxel_dimensions': [float(v) for v in voxel_dimensions],
        'data_type': data_type,
        'volume_shape': volume_shape,
        'min_value': min_value,
        'max_value': max_value,
        'mean_value': mean_value,
        'std_value': std_value,
        'variance': variance,
        'first_voxel': first_voxel,
        'calibration_min': calibration_min,
        'calibration_max': calibration_max,
        'voxel_offset': voxel_offset,
        'slope': slope,
        'intercept': intercept,
        'unique_values': unique_values,
        'unique_values_truncated': unique_values_truncated,
        'total_unique_count': total_unique_count,
        'processing_time_ms': processing_time,
    }


def extract_unique_values(
    volume: np.ndarray,
    max_threshold: int,
    max_display: int
) -> Tuple[List[float], int, bool]:
    """
    Extract unique values with early exit optimization.
    Returns: (unique_values_list, total_count, truncated_flag)
    """
    # Strategy: Scan through volume with early exit if we find > max_threshold unique values
    unique_set = set()
    exceeded_threshold = False

    # Flatten and iterate with early exit
    flat_volume = volume.flat
    for val in flat_volume:
        if np.isfinite(val):
            unique_set.add(float(val))

            # Early exit: stop scanning if we exceed threshold
            if len(unique_set) > max_threshold:
                exceeded_threshold = True
                break

    if exceeded_threshold:
        # Too many unique values - don't collect them all
        return [], 0, True
    else:
        # Few enough unique values - provide the full list
        total_count = len(unique_set)
        truncated = total_count > max_display

        # Sort and truncate
        unique_values = sorted(unique_set)[:max_display]

        return unique_values, total_count, truncated


def print_text_output(stats: Dict) -> None:
    """Print statistics in human-readable text format."""
    print("=== NIfTI File Processor ===")
    print(f"NIfTI File: {stats['file_path']}")
    print("----------------------------------------")
    print(f"Dimensions: {stats['dimensions']}")
    if len(stats['dimensions']) >= 3:
        print(f"Dimensions: {stats['dimensions'][0]} x {stats['dimensions'][1]} x {stats['dimensions'][2]}")
    print(f"Data type: {stats['data_type']}")
    if stats['voxel_dimensions']:
        print(f"Voxel dimensions: {stats['voxel_dimensions']} mm")
    print(f"Volume shape: {stats['volume_shape']}")
    print(f"First voxel value: {stats['first_voxel']}")
    print(f"Min voxel value: {stats['min_value']}")
    print(f"Max voxel value: {stats['max_value']}")
    print(f"Mean voxel value: {stats['mean_value']}")
    print(f"Standard deviation: {stats['std_value']}")
    print(f"Variance: {stats['variance']}")
    print(f"Calibration: ({stats['calibration_min']}, {stats['calibration_max']})")
    print(f"Voxel offset: {stats['voxel_offset']}")

    # Print unique values
    if stats['total_unique_count'] == 0 and stats['unique_values_truncated']:
        # Exceeded threshold - too many unique values
        print("Unique values: >200 (too many to display)")
    elif stats['total_unique_count'] > 0:
        print(f"Unique values (total: {stats['total_unique_count']}):")
        if stats['unique_values_truncated']:
            print(f"  [Showing first {len(stats['unique_values'])} of {stats['total_unique_count']} unique values]")

        # Format unique values in a compact way
        VALUES_PER_LINE = 10
        unique_vals = stats['unique_values']

        for i in range(0, len(unique_vals), VALUES_PER_LINE):
            chunk = unique_vals[i:i + VALUES_PER_LINE]
            if i // VALUES_PER_LINE < 5 or not stats['unique_values_truncated']:
                formatted = ', '.join(f'{val:.3f}' for val in chunk)
                print(f"  {formatted}")

        if stats['unique_values_truncated'] and len(unique_vals) > VALUES_PER_LINE * 5:
            remaining = len(unique_vals) - VALUES_PER_LINE * 5
            print(f"  ... ({remaining} more values)")
    else:
        print("Unique values: 0 (no valid values found)")

    print(f"Processing time: {stats['processing_time_ms']:.2f} ms")
    print("----------------------------------------")
    print("Successfully processed NIfTI file.")


def process_batch(batch_file: str, output_format: str) -> None:
    """Process multiple NIfTI files listed in a batch file."""
    with open(batch_file, 'r') as f:
        files = [line.strip() for line in f if line.strip()]

    results = []

    for file_path in files:
        try:
            stats = process_nifti_file(file_path)
            results.append(stats)
        except Exception as e:
            error_result = {
                'error': str(e),
                'file_path': file_path,
            }
            results.append(error_result)

    if output_format == 'json':
        print(json.dumps(results, indent=2))
    else:
        print(f"Processed {len(results)} files. Use --output-format json for structured output.")


def main():
    parser = argparse.ArgumentParser(
        description='Process NIfTI files with optional JSON output'
    )
    parser.add_argument(
        'input',
        nargs='?',
        default='data/avg152T1.nii',
        help='Input NIfTI file'
    )
    parser.add_argument(
        '--output-format',
        choices=['text', 'json'],
        default='text',
        help='Output format: text or json'
    )
    parser.add_argument(
        '--batch-file',
        help='Process multiple files listed in a text file'
    )

    args = parser.parse_args()

    # Handle batch processing
    if args.batch_file:
        process_batch(args.batch_file, args.output_format)
        return

    # Single file processing
    file_path = args.input

    if not Path(file_path).exists():
        error = {
            'error': f"File '{file_path}' not found",
            'file_path': file_path,
        }

        if args.output_format == 'json':
            print(json.dumps(error, indent=2))
        else:
            print(f"Error: {error['error']}")
        sys.exit(1)

    try:
        stats = process_nifti_file(file_path)

        if args.output_format == 'json':
            print(json.dumps(stats, indent=2))
        else:
            print_text_output(stats)

    except Exception as e:
        error = {
            'error': str(e),
            'file_path': file_path,
        }

        if args.output_format == 'json':
            print(json.dumps(error, indent=2))
        else:
            print(f"Error: {error['error']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
