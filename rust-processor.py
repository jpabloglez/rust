#!/usr/bin/env python3
"""
Different strategies for integrating Rust performance into Python projects.

This module demonstrates various approaches from simple subprocess calls
to advanced Python extensions using PyO3.
"""

import subprocess
import json
import sys
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import numpy as np


# =============================================================================
# Strategy 1: Simple stdout parsing (easiest to implement)
# =============================================================================

class RustNiftiProcessor:
    """
    Simple wrapper that calls Rust binary and parses stdout output.
    
    Pros: Easy to implement, no compilation complexity
    Cons: Parsing overhead, less robust, limited data transfer
    """
    
    def __init__(self, rust_binary_path: str = "./target/release/nifti-processor"):
        """
        Initialize the processor with path to Rust binary.
        
        Parameters
        ----------
        rust_binary_path : str
            Path to the compiled Rust binary
        """
        self.rust_binary_path = rust_binary_path
        
    def process_nifti(self, file_path: str) -> Dict[str, Any]:
        """
        Process NIfTI file using Rust binary and parse results.
        
        Parameters
        ----------
        file_path : str
            Path to NIfTI file to process
            
        Returns
        -------
        dict
            Dictionary containing parsed statistics and metadata
        """
        try:
            # Run Rust binary and capture output
            result = subprocess.run(
                [self.rust_binary_path, file_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the stdout output
            return self._parse_output(result.stdout)
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Rust processor failed: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError(f"Rust binary not found at {self.rust_binary_path}")
    
    def _parse_output(self, output: str) -> Dict[str, Any]:
        """
        Parse stdout output from Rust binary.
        
        Parameters
        ----------
        output : str
            Raw stdout output from Rust binary
            
        Returns
        -------
        dict
            Parsed data dictionary
        """
        parsed = {}
        lines = output.strip().split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                
                # Try to convert to appropriate type
                try:
                    if 'x' in value and 'dimensions' in key:
                        # Parse "512 x 512 x 181" format
                        dims = [int(x.strip()) for x in value.split('x')]
                        parsed[key] = dims
                    elif value.replace('.', '').replace('-', '').isdigit():
                        # Numeric value
                        parsed[key] = float(value) if '.' in value else int(value)
                    else:
                        parsed[key] = value
                except ValueError:
                    parsed[key] = value
        
        return parsed


# =============================================================================
# Strategy 2: JSON output (better structured data transfer)
# =============================================================================

class RustNiftiProcessorJSON:
    """
    Wrapper that expects Rust binary to output structured JSON.
    
    Pros: Robust data transfer, type safety, easy parsing
    Cons: Requires modifying Rust code to output JSON
    """
    
    def __init__(self, rust_binary_path: str = "./target/release/nifti-processor-json"):
        """
        Initialize processor expecting JSON output.
        
        Parameters
        ----------
        rust_binary_path : str
            Path to Rust binary that outputs JSON
        """
        self.rust_binary_path = rust_binary_path
        
    def process_nifti(self, file_path: str) -> Dict[str, Any]:
        """
        Process NIfTI file and parse JSON output.
        
        Parameters
        ----------
        file_path : str
            Path to NIfTI file
            
        Returns
        -------
        dict
            Parsed JSON data
        """
        try:
            result = subprocess.run(
                [self.rust_binary_path, file_path, "--output-format", "json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            return json.loads(result.stdout)
            
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON output from Rust: {e}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Rust processor failed: {e.stderr}")


# =============================================================================
# Strategy 3: File-based data transfer (for large datasets)
# =============================================================================

class RustNiftiProcessorFile:
    """
    Use temporary files to transfer large datasets between Python and Rust.
    
    Pros: Can handle large data, robust, supports binary data
    Cons: I/O overhead, temporary file management
    """
    
    def __init__(self, rust_binary_path: str = "./target/release/nifti-processor"):
        """
        Initialize processor with file-based data transfer.
        
        Parameters
        ----------
        rust_binary_path : str
            Path to Rust binary
        """
        self.rust_binary_path = rust_binary_path
        
    def process_nifti_with_data(self, file_path: str) -> tuple[Dict[str, Any], np.ndarray]:
        """
        Process NIfTI file and return both metadata and volume data.
        
        Parameters
        ----------
        file_path : str
            Path to NIfTI file
            
        Returns
        -------
        tuple
            (metadata_dict, volume_array)
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Output files
            metadata_file = os.path.join(temp_dir, "metadata.json")
            volume_file = os.path.join(temp_dir, "volume.npy")
            
            try:
                # Run Rust with output file arguments
                result = subprocess.run([
                    self.rust_binary_path,
                    file_path,
                    "--metadata-output", metadata_file,
                    "--volume-output", volume_file
                ], check=True, capture_output=True, text=True)
                
                # Load results
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    
                volume = np.load(volume_file)
                
                return metadata, volume
                
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Rust processor failed: {e.stderr}")


# =============================================================================
# Strategy 4: PyO3 Python Extension (most efficient)
# =============================================================================

# This would be implemented in Rust using PyO3 crate
# Here's what the Python interface would look like:

"""
Example of what PyO3 integration would provide:

```python
import rust_nifti  # This would be the compiled PyO3 extension

# Direct function calls with zero-copy data transfer
metadata = rust_nifti.get_metadata("data/brain.nii")
volume = rust_nifti.load_volume("data/brain.nii")  # Returns numpy array directly
stats = rust_nifti.compute_stats("data/brain.nii")

# Or class-based interface
processor = rust_nifti.NiftiProcessor()
result = processor.process("data/brain.nii")
```

To implement this, you'd need to:
1. Add PyO3 to Cargo.toml
2. Create Python-compatible functions in Rust
3. Build as Python extension module
"""


# =============================================================================
# Strategy 5: Batch processing for maximum efficiency
# =============================================================================

class BatchRustProcessor:
    """
    Process multiple files in a single Rust call for maximum efficiency.
    
    Pros: Minimal startup overhead, efficient for large datasets
    Cons: More complex error handling, all-or-nothing processing
    """
    
    def __init__(self, rust_binary_path: str = "./target/release/nifti-batch-processor"):
        """
        Initialize batch processor.
        
        Parameters
        ----------
        rust_binary_path : str
            Path to batch-capable Rust binary
        """
        self.rust_binary_path = rust_binary_path
        
    def process_batch(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple NIfTI files in a single Rust call.
        
        Parameters
        ----------
        file_paths : list of str
            List of NIfTI file paths to process
            
        Returns
        -------
        list of dict
            Results for each file
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            # Write file list
            for path in file_paths:
                f.write(f"{path}\n")
            file_list_path = f.name
            
        try:
            result = subprocess.run([
                self.rust_binary_path,
                "--batch-file", file_list_path,
                "--output-format", "json"
            ], capture_output=True, text=True, check=True)
            
            return json.loads(result.stdout)
            
        finally:
            os.unlink(file_list_path)


# =============================================================================
# Usage examples and performance comparison
# =============================================================================

def demonstrate_strategies():
    """Demonstrate different integration strategies."""
    
    print("=== Rust-Python Integration Strategies Demo ===\n")
    
    file_path = "data/avg152T1.nii"
    
    # Strategy 1: Simple stdout parsing
    print("1. Simple stdout parsing:")
    try:
        processor1 = RustNiftiProcessor()
        result1 = processor1.process_nifti(file_path)
        print(f"   Min value: {result1.get('min_voxel_value', 'N/A')}")
        print(f"   Max value: {result1.get('max_voxel_value', 'N/A')}")
    except RuntimeError as e:
        print(f"   Error: {e}")
    
    print()
    
    # Strategy 2: JSON output
    print("2. JSON structured output:")
    try:
        processor2 = RustNiftiProcessorJSON()
        result2 = processor2.process_nifti(file_path)
        print(f"   Successfully parsed JSON with {len(result2)} fields")
    except RuntimeError as e:
        print(f"   Error: {e}")
    
    print()
    
    # Strategy 3: File-based transfer
    print("3. File-based data transfer:")
    try:
        processor3 = RustNiftiProcessorFile()
        metadata, volume = processor3.process_nifti_with_data(file_path)
        print(f"   Volume shape: {volume.shape}")
        print(f"   Volume dtype: {volume.dtype}")
    except RuntimeError as e:
        print(f"   Error: {e}")
    
    print()
    
    # Strategy 5: Batch processing
    print("4. Batch processing:")
    try:
        batch_processor = BatchRustProcessor()
        results = batch_processor.process_batch([file_path, file_path])
        print(f"   Processed {len(results)} files in batch")
    except RuntimeError as e:
        print(f"   Error: {e}")


def performance_recommendations():
    """Print performance recommendations for different use cases."""
    
    print("\n=== Performance Recommendations ===\n")
    
    recommendations = {
        "Single file, simple stats": "Strategy 1 (stdout parsing) - simplest implementation",
        "Single file, complex data": "Strategy 3 (file transfer) or PyO3 extension",
        "Many small files": "Strategy 5 (batch processing) - minimize startup overhead",
        "Real-time processing": "PyO3 extension - zero-copy, in-process calls",
        "Production deployment": "PyO3 extension - most robust and performant",
        "Prototyping/research": "Strategy 1 or 2 - quick to implement"
    }
    
    for use_case, recommendation in recommendations.items():
        print(f"• {use_case}: {recommendation}")
    
    print("\nGeneral guidelines:")
    print("• Use subprocess for < 10 files or prototyping")
    print("• Use PyO3 for production or > 100 files")
    print("• Use batch processing for 10-100 files")
    print("• Consider memory usage: file transfer vs in-memory")


if __name__ == "__main__":
    # Para uso inmediato - parsing de stdout
    processor = RustNiftiProcessor("./target/debug/nifti-stats")
    stats = processor.process_nifti("data/avg152T1.nii")
    #min_val = stats['min_voxel_value']
    print("Statistics from Rust binary:", stats)
    #demonstrate_strategies()
    #performance_recommendations()