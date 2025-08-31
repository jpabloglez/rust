# Rust Training Application

This is a comprehensive Rust training application that demonstrates fundamental concepts of the Rust programming language.

## Features

- **Variables and Mutability**: Examples of immutable and mutable variables, shadowing
- **Data Types**: Scalar types (integers, floats, booleans, characters) and compound types (tuples, arrays)
- **Flow Control**: Conditionals, loops (loop, while, for), and iterators
- **Functions**: Function definitions, parameters, return values
- **Match Control Flow**: Pattern matching with match expressions
- **Enumerations**: Defining and using enums with different kinds of variants
- **Ownership**: Rust's ownership system, borrowing, and references
- **Error Handling**: Using Result and Option types for error handling
- **Closures**: Anonymous functions that can capture their environment
- **Concurrency**: Thread spawning, sharing state between threads with Arc and Mutex
- **NIfTI File Processing**: Example of working with NIfTI files for scientific computing

## Prerequisites

- Docker (recommended)
- Rust and Cargo (if not using Docker)

## Building and Running with Docker (Recommended)

1. Build and start the container:
   ```bash
   docker-compose up -d --build
   ```

2. Build the project:
   ```bash
   docker exec rust cargo build
   ```

3. Run the examples:
   ```bash
   # Hello World example
   docker exec rust ./target/debug/hello
   
   # Comprehensive Rust concepts example
   docker exec rust ./target/debug/vars
   
   # NIfTI file processor (requires a NIfTI file in the data directory)
   docker exec rust ./target/debug/nifti-example
   ```

## Building Individual Files with rustc

Note: Examples that use external dependencies (like the NIfTI example) must be built with Cargo, not rustc directly.

For simple examples without dependencies:
```bash
# Compile hello.rs (no external dependencies)
docker exec rust rustc src/hello.rs -o build/hello
docker exec rust ./build/hello
```

For examples with dependencies, use Cargo:
```bash
# Build with Cargo (recommended for all examples)
docker exec rust cargo build
# Then run the binaries from target/debug/
```

## Running Tests

To run the included tests:

```bash
docker exec rust cargo test
```

## Dependencies

- `nifti = "0.14.0"`: For NIfTI file handling

## Project Structure

```
.
├── Cargo.toml              # Project configuration and dependencies
├── docker-compose.yml      # Docker configuration
├── README.md               # This file
├── GUIDE.md                # Detailed guide on Rust concepts
├── QWEN.md                 # Project context for Qwen Code
├── setup/
│   └── Dockerfile.rust     # Docker image definition
├── src/
│   ├── hello.rs            # Basic "Hello, World!" example
│   ├── vars.rs             # Comprehensive Rust concepts example
│   ├── nifti.rs            # NIfTI file processing example
│   └── lib.rs              # Library code
├── build/                  # Compiled binaries (when using rustc)
├── target/                 # Compiled binaries (when using cargo)
└── data/                   # Data files (NIfTI files go here)
    └── README.md           # Instructions for obtaining sample data
```

## Adding New Features

To add new functionality:

1. Create a new source file in the `src/` directory
2. Add a `[[bin]]` entry in `Cargo.toml` if it's a binary
3. Build with `docker exec rust cargo build`

## Troubleshooting

If you encounter any issues:

1. Make sure Docker is running
2. Rebuild the container with `docker-compose up -d --build`
3. Check that all dependencies are properly installed with `docker exec rust cargo build`

Note: When using `rustc` directly, it won't have access to dependencies defined in `Cargo.toml`. For examples that use external crates, always use `cargo build` instead.