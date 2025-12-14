// Add to Cargo.toml:
// [dependencies]
// serde = { version = "1.0", features = ["derive"] }
// serde_json = "1.0"
// clap = { version = "4.0", features = ["derive"] }
// ndarray-stats = "0.5"
// ordered-float = "4.0"

extern crate nifti;

use nifti::{NiftiObject, ReaderOptions, IntoNdArray};
use serde::{Deserialize, Serialize};
use std::path::Path;
use clap::{Arg, Command};

#[derive(Serialize, Deserialize, Debug)]
struct NiftiStats {
    file_path: String,
    dimensions: Vec<usize>,
    voxel_dimensions: Vec<f32>,
    data_type: String,
    volume_shape: Vec<usize>,
    min_value: f32,
    max_value: f32,
    mean_value: f32,
    std_value: f32,
    variance: f32,
    first_voxel: f32,
    calibration_min: f32,
    calibration_max: f32,
    voxel_offset: f32,
    slope: f32,
    intercept: f32,
    unique_values: Vec<f32>,
    unique_values_truncated: bool,
    total_unique_count: usize,
    processing_time_ms: f64,
}

#[derive(Serialize, Deserialize, Debug)]
struct ProcessingError {
    error: String,
    file_path: String,
}

fn process_nifti_file(file_path: &str) -> Result<NiftiStats, Box<dyn std::error::Error>> {
    let start_time = std::time::Instant::now();

    // Read the NIfTI file
    let obj = ReaderOptions::new().read_file(file_path)?;
    let header = obj.header();

    // Extract basic information - convert u16 to usize
    let dims = header.dim()?;
    let dimensions: Vec<usize> = dims.iter().map(|&x| x as usize).collect();

    let pixdim = &header.pixdim;
    let voxel_dimensions = if pixdim.len() >= 4 {
        pixdim[1..4].to_vec()
    } else {
        vec![]
    };

    let data_type = format!("{:?}", header.data_type()?);

    // Extract header values before moving obj
    let calibration_min = header.cal_min;
    let calibration_max = header.cal_max;
    let voxel_offset = header.vox_offset;
    let slope = header.scl_slope;
    let intercept = header.scl_inter;

    // Process volume data (this moves obj)
    use ndarray_stats::QuantileExt;
    let volume = obj.into_volume().into_ndarray::<f32>()?;
    let volume_shape = volume.shape().to_vec();

    // Compute statistics efficiently - handle Result types properly
    let first_voxel = volume[[0; 3]];
    let min_value = *volume.min().unwrap_or(&f32::NAN);
    let max_value = *volume.max().unwrap_or(&f32::NAN);
    let mean_value = volume.mean().unwrap_or(f32::NAN);
    let std_value = volume.std(0.0);
    let variance = volume.var(0.0);

    // Extract unique values with early exit optimization
    // Only collect unique values if there are fewer than 200 different values
    const MAX_UNIQUE_THRESHOLD: usize = 200; // Stop if we exceed this
    const MAX_DISPLAY_VALUES: usize = 100;   // Limit for display output

    use std::collections::HashSet;

    let total_unique_count: usize;
    let unique_values: Vec<f32>;
    let unique_values_truncated: bool;

    // Strategy: Scan through volume with early exit if we find > 200 unique values
    let mut unique_set: HashSet<ordered_float::OrderedFloat<f32>> = HashSet::new();
    let mut exceeded_threshold = false;

    for &val in volume.iter() {
        if !val.is_nan() && !val.is_infinite() {
            unique_set.insert(ordered_float::OrderedFloat(val));

            // Early exit: stop scanning if we exceed threshold
            if unique_set.len() > MAX_UNIQUE_THRESHOLD {
                exceeded_threshold = true;
                break;
            }
        }
    }

    if exceeded_threshold {
        // Too many unique values - don't collect them all
        total_unique_count = 0; // Indicate we didn't count all
        unique_values = Vec::new();
        unique_values_truncated = true;
    } else {
        // Few enough unique values - provide the full list
        total_unique_count = unique_set.len();
        unique_values_truncated = total_unique_count > MAX_DISPLAY_VALUES;

        // Convert and sort
        let mut values: Vec<f32> = unique_set.iter()
            .map(|&x| x.into_inner())
            .collect();
        values.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));

        // Truncate to display limit
        values.truncate(MAX_DISPLAY_VALUES);
        unique_values = values;
    }

    let processing_time = start_time.elapsed().as_secs_f64() * 1000.0; // Convert to milliseconds

    Ok(NiftiStats {
        file_path: file_path.to_string(),
        dimensions,
        voxel_dimensions,
        data_type,
        volume_shape,
        min_value,
        max_value,
        mean_value,
        std_value,
        variance,
        first_voxel,
        calibration_min,
        calibration_max,
        voxel_offset,
        slope,
        intercept,
        unique_values,
        unique_values_truncated,
        total_unique_count,
        processing_time_ms: processing_time,
    })
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("NIfTI Processor")
        .version("1.0")
        .author("JPG")
        .about("Process NIfTI files with optional JSON output")
        .arg(Arg::new("INPUT")
            .help("Input NIfTI file")
            .required(true)
            .index(1))
        .arg(Arg::new("output-format")
            .long("output-format")
            .help("Output format: text or json")
            .value_parser(["text", "json"])
            .default_value("text"))
        .arg(Arg::new("batch-file")
            .long("batch-file")
            .help("Process multiple files listed in a text file")
            .value_name("FILE"))
        .get_matches();

    let output_format = matches.get_one::<String>("output-format").unwrap();
    
    // Handle batch processing
    if let Some(batch_file) = matches.get_one::<String>("batch-file") {
        return process_batch(batch_file, output_format);
    }
    
    // Single file processing
    let file_path = if let Some(input) = matches.get_one::<String>("INPUT") {
        input.clone()
    } else {
        "data/avg152T1.nii".to_string()
    };
    
    if !Path::new(&file_path).exists() {
        let error = ProcessingError {
            error: format!("File '{}' not found", file_path),
            file_path: file_path.clone(),
        };
        
        if output_format == "json" {
            println!("{}", serde_json::to_string_pretty(&error)?);
        } else {
            println!("Error: {}", error.error);
        }
        return Ok(());
    }
    
    match process_nifti_file(&file_path) {
        Ok(stats) => {
            if output_format == "json" {
                println!("{}", serde_json::to_string_pretty(&stats)?);
            } else {
                print_text_output(&stats);
            }
        }
        Err(e) => {
            let error = ProcessingError {
                error: e.to_string(),
                file_path,
            };
            
            if output_format == "json" {
                println!("{}", serde_json::to_string_pretty(&error)?);
            } else {
                println!("Error: {}", error.error);
            }
        }
    }
    
    Ok(())
}

fn process_batch(batch_file: &str, output_format: &str) -> Result<(), Box<dyn std::error::Error>> {
    use std::fs;
    
    let content = fs::read_to_string(batch_file)?;
    let files: Vec<&str> = content.lines().filter(|line| !line.trim().is_empty()).collect();
    
    let mut results = Vec::new();
    
    for file_path in files {
        let result = match process_nifti_file(file_path.trim()) {
            Ok(stats) => serde_json::Value::Object(serde_json::to_value(stats)?.as_object().unwrap().clone()),
            Err(e) => {
                let error = ProcessingError {
                    error: e.to_string(),
                    file_path: file_path.to_string(),
                };
                serde_json::to_value(error)?
            }
        };
        results.push(result);
    }
    
    if output_format == "json" {
        println!("{}", serde_json::to_string_pretty(&results)?);
    } else {
        println!("Processed {} files. Use --output-format json for structured output.", results.len());
    }
    
    Ok(())
}

fn print_text_output(stats: &NiftiStats) {
    println!("=== NIfTI File Processor ===");
    println!("NIfTI File: {}", stats.file_path);
    println!("----------------------------------------");
    println!("Dimensions: {:?}", stats.dimensions);
    if stats.dimensions.len() >= 3 {
        println!("Dimensions: {} x {} x {}", stats.dimensions[0], stats.dimensions[1], stats.dimensions[2]);
    }
    println!("Data type: {}", stats.data_type);
    if !stats.voxel_dimensions.is_empty() {
        println!("Voxel dimensions: {:?} mm", stats.voxel_dimensions);
    }
    println!("Volume shape: {:?}", stats.volume_shape);
    println!("First voxel value: {}", stats.first_voxel);
    println!("Min voxel value: {}", stats.min_value);
    println!("Max voxel value: {}", stats.max_value);
    println!("Mean voxel value: {}", stats.mean_value);
    println!("Standard deviation: {}", stats.std_value);
    println!("Variance: {}", stats.variance);
    println!("Calibration: ({}, {})", stats.calibration_min, stats.calibration_max);
    println!("Voxel offset: {}", stats.voxel_offset);

    // Print unique values
    if stats.total_unique_count == 0 && stats.unique_values_truncated {
        // Exceeded threshold - too many unique values
        println!("Unique values: >200 (too many to display)");
    } else if stats.total_unique_count > 0 {
        println!("Unique values (total: {}):", stats.total_unique_count);
        if stats.unique_values_truncated {
            println!("  [Showing first {} of {} unique values]", stats.unique_values.len(), stats.total_unique_count);
        }

        // Format unique values in a compact way
        const VALUES_PER_LINE: usize = 10;
        for (i, chunk) in stats.unique_values.chunks(VALUES_PER_LINE).enumerate() {
            if i < 5 || !stats.unique_values_truncated { // Show first 5 lines or all if not truncated
                print!("  ");
                for (j, val) in chunk.iter().enumerate() {
                    if j > 0 {
                        print!(", ");
                    }
                    print!("{:.3}", val);
                }
                println!();
            }
        }
        if stats.unique_values_truncated && stats.unique_values.len() > VALUES_PER_LINE * 5 {
            println!("  ... ({} more values)", stats.unique_values.len() - VALUES_PER_LINE * 5);
        }
    } else {
        println!("Unique values: 0 (no valid values found)");
    }

    println!("Processing time: {:.2} ms", stats.processing_time_ms);
    println!("----------------------------------------");
    println!("Successfully processed NIfTI file.");
}