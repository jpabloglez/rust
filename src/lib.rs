//! # Rust Training Library
//!
//! This library contains utilities and examples for learning Rust.
//!
//! ## Modules
//!
//! - `vars` - Examples of variables, data types, flow control, functions, ownership, and concurrency
//! - `nifti` - NIfTI file processing utilities
//!
//! ## Usage
//!
//! This library is primarily intended for educational purposes, demonstrating
//! various Rust concepts and features.

/// Examples of variables, mutability, data types, flow control, functions,
/// ownership, and concurrency.
pub mod vars {
    /// Demonstrates variable mutability and shadowing
    pub fn variables() {
        let x = 5;
        println!("Immutable x: {}", x);
        
        let mut y = 5;
        println!("Mutable y: {}", y);
        y = 10;
        println!("Modified y: {}", y);
        
        // Shadowing
        let z = 5;
        let z = z + 1;
        let z = z * 2;
        println!("Shadowed z: {}", z);
    }
    
    /// Demonstrates basic data types
    pub fn data_types() {
        let integer: i32 = 42;
        let float: f64 = 3.14159;
        let boolean: bool = true;
        let character: char = 'R';
        
        println!("Integer: {}, Float: {}, Boolean: {}, Character: {}", 
                 integer, float, boolean, character);
    }
    
    /// Simple function that adds two integers
    pub fn add(a: i32, b: i32) -> i32 {
        a + b
    }
}

/// NIfTI file processing utilities
pub mod nifti {
    /// Placeholder for NIfTI functionality
    pub fn process_file(_path: &str) -> Result<(), Box<dyn std::error::Error>> {
        println!("Processing NIfTI file: {}", _path);
        // In a real implementation, this would contain actual NIfTI processing code
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(vars::add(2, 3), 5);
        assert_eq!(vars::add(-1, 1), 0);
    }
}
