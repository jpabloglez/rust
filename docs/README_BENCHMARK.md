# NIfTI Statistics - Rust vs Python Performance Comparison

This directory contains both Rust and Python implementations of a NIfTI statistics processor, along with benchmarking tools.

## Files

- `src/nifti-stats.rs` - Rust implementation
- `nifti_stats.py` - Python implementation (requires nibabel, numpy)
- `benchmark_comparison.py` - Performance comparison script

## Setup

### Rust Version
```bash
# Build the Rust binary
cargo build --bin nifti-stats

# Or build with optimizations
cargo build --release --bin nifti-stats
```

### Python Version
```bash
# Install required packages (use conda environment if available)
pip install nibabel numpy
```

## Running the Benchmark

**Important**: Make sure to run the benchmark script with a Python interpreter that has `nibabel` and `numpy` installed.

If you're using a conda environment (e.g., `neuro`):

```bash
# Activate your conda environment first
conda activate neuro

# Run the benchmark
python benchmark_comparison.py data/avg152T1.nii 5
```

If you're using system Python with packages installed:

```bash
python3 benchmark_comparison.py data/avg152T1.nii 5
```

The second argument (5) is the number of runs for averaging.

## Running Individual Versions

### Rust Version

```bash
# Debug build
./target/debug/nifti-stats data/avg152T1.nii

# Release build (faster)
./target/release/nifti-stats data/avg152T1.nii

# JSON output
./target/debug/nifti-stats data/avg152T1.nii --output-format json
```

### Python Version

```bash
# Make sure you're using Python with nibabel installed
python nifti_stats.py data/avg152T1.nii

# JSON output
python nifti_stats.py data/avg152T1.nii --output-format json
```

## Performance Optimizations

Both implementations include the same optimization strategy:
- **Early exit**: Stops collecting unique values after finding >200 unique values
- **HashSet for deduplication**: O(1) average insertion time
- **Sorted output**: Only sorts the values that will be displayed

### Why the Early Exit Matters

For different types of medical images:

| Image Type | Typical Unique Values | Speedup |
|------------|----------------------|---------|
| Label/Segmentation maps | 5-50 | 1x (must scan all) |
| Discrete atlases | 50-200 | 1x (must scan all) |
| CT scans (HU values) | 10,000+ | **~1000x** (exits early) |
| MRI T1/T2 weighted | 10,000+ | **~1000x** (exits early) |

## Expected Results

The Rust version should be faster due to:
1. Compiled native code vs interpreted Python
2. Lower memory overhead
3. More efficient execution

However, both benefit equally from the early-exit optimization for images with many unique values.

## Troubleshooting

### Python: "ModuleNotFoundError: No module named 'nibabel'"

Install nibabel in your Python environment:
```bash
pip install nibabel numpy
```

Or use a conda environment:
```bash
conda create -n neuro python=3.10
conda activate neuro
pip install nibabel numpy
```

### Rust: "cargo: command not found"

Install Rust from https://rustup.rs/

### Benchmark fails to find Rust binary

Build the Rust binary first:
```bash
cargo build --bin nifti-stats
```
