# Rust Training Application

This is a comprehensive Rust training application that demonstrates fundamental concepts of the Rust programming language, including variables, data types, flow control, functions, ownership, and concurrency. It also includes an example of NIfTI file handling for scientific computing applications.

## Project Structure

- `src/hello.rs` - Basic "Hello, World!" example
- `src/vars.rs` - Comprehensive examples of Rust concepts
- `src/nifti.rs` - NIfTI file processing example
- `Cargo.toml` - Project configuration and dependencies

## Building and Running with Docker (Recommended)

### 1. Build and Start Container
```bash
docker-compose up -d --build
```

### 2. Build All Binaries with Cargo
```bash
docker exec rust cargo build
```

### 3. Run the Examples

Run the "Hello, World!" example:
```bash
docker exec rust ./target/debug/hello
```

Run the comprehensive Rust concepts example:
```bash
docker exec rust ./target/debug/vars
```

Run the NIfTI file processor (provide a NIfTI file in the data directory):
```bash
docker exec rust ./target/debug/nifti-example
```

## Building Individual Files with rustc

Note: The NIfTI example requires dependencies that are managed by Cargo. To compile individual files that don't have external dependencies:

```bash
# Compile hello.rs (no external dependencies)
docker exec rust rustc src/hello.rs -o build/hello
docker exec rust ./build/hello
```

For files with dependencies, use Cargo instead:

```bash
# Build with Cargo (recommended for all examples)
docker exec rust cargo build
# Then run the binaries from target/debug/
```

## Creating a New Project

To create a new binary Rust project:
```bash
cargo new --bin [PROJECT-NAME]
```

## Managing Dependencies

Dependencies are managed through Cargo.toml. To add new dependencies:

1. Edit the `Cargo.toml` file to include the desired packages under `[dependencies]`
2. Run `docker exec rust cargo build` to install the dependencies and rebuild the project

## Project Information

This project uses:
- Rust 2021 edition
- NIfTI crate version 0.14.0 for NIfTI file handling
- Docker for consistent development environment