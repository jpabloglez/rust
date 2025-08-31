# Rust Training Application - Context for Qwen Code

## Project Overview

This directory contains a Rust training application designed to demonstrate fundamental concepts of the Rust programming language. It includes examples for variables, data types, flow control, functions, ownership, and concurrency. The project also incorporates NIfTI file handling, indicating a potential use case in scientific computing or medical imaging.

The project uses Docker for containerization, ensuring a consistent development environment. It's structured with a `src` directory for source code, a `build` directory for compiled binaries, and a `setup` directory for Docker configurations.

## Key Technologies

- **Rust:** The primary programming language.
- **Docker:** Used for containerization and environment setup.
- **NIfTI crate:** For handling NIfTI files (`nifti = "0.14.0"`).
- **Cargo:** Rust's package manager and build system.

## Project Structure

- `src/`: Contains Rust source files.
  - `hello.rs`: A basic "Hello, World!" program.
  - `vars.rs`: Examples of variables, mutability, data types, flow control, functions, ownership, and concurrency.
  - `nifti.rs`: Example program for loading and processing NIfTI files.
- `setup/`: Contains Docker setup files.
  - `Dockerfile.rust`: Defines the Rust development environment.
- `build/`: Directory for compiled binaries.
- `data/`: Intended for data files (e.g., `dwi.nii.gz` for the NIfTI example).
- `Cargo.toml`: Project configuration, dependencies, and binary definitions.

## Building and Running

### Using Docker (Recommended)

1.  **Build and Start Container:**
    ```bash
    docker-compose up -d --build
    ```
    This command builds the Docker image and starts the container named `rust`.

2.  **Compile a Script:**
    To compile `src/hello.rs` and output the binary to `build/hello`:
    ```bash
    docker exec -it rust rustc src/hello.rs -o build/hello
    ```

3.  **Run a Compiled Program:**
    To run the compiled `hello` program:
    ```bash
    docker exec -it rust ./build/hello
    ```

4.  **Using Cargo:**
    To build the project using Cargo (which will compile the binaries defined in `Cargo.toml`):
    ```bash
    docker exec -it rust cargo build
    ```
    The resulting binaries will be placed in the `target/debug/` directory inside the container.

### Creating a New Project

To create a new binary Rust project:
```bash
cargo new --bin [PROJECT-NAME]
```

### Installing Dependencies

To add dependencies:
1.  Edit the `Cargo.toml` file to include the desired packages under `[dependencies]`.
2.  Run `docker exec -it rust cargo build` to install the dependencies and rebuild the project.

## Development Conventions

- **Rust Edition:** The project uses the 2021 edition of Rust.
- **Binary Definitions:** Binaries are explicitly defined in `Cargo.toml` under `[[bin]]`.
- **Source Code:** Source files are located in the `src` directory.
- **Containerization:** Development and execution are intended to be done within the provided Docker container to ensure consistency.