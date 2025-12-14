# Testing Release Build Performance

The current benchmark uses the **debug build** which is unoptimized.

## Quick Test

Build with release optimizations:
```bash
cargo build --release --bin nifti-stats
```

Then compare:
```bash
# Debug build
time ./target/debug/nifti-stats data/avg152T1.nii > /dev/null

# Release build
time ./target/release/nifti-stats data/avg152T1.nii > /dev/null
```

Expected improvement: **2-10x faster** for release build

## Why Release Build Matters

Rust debug builds include:
- No optimizations
- Bounds checking on every array access
- No function inlining
- No SIMD vectorization

Release builds enable:
- LLVM optimizations (O3 level)
- Aggressive inlining
- Auto-vectorization (SIMD)
- Dead code elimination

This is why the Python version (always "optimized") beats Rust debug builds for internal processing.

## Answer to Your Question

**Would NumPy-equivalent improve efficiency?**

1. **For release builds**: Probably not much - the bottleneck is file I/O, not math
2. **For debug builds**: Yes, but just use release build instead
3. **Best approach**:
   - Use `cargo build --release` (10x easier than adding BLAS)
   - This should make Rust **faster than Python for both external AND internal processing**

The real lesson: **Always benchmark release builds**, not debug builds!
