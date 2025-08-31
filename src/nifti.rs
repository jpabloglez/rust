extern crate nifti;

use nifti::{NiftiObject, ReaderOptions, NiftiType, NiftiVolume};
use std::env;
use std::path::Path;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("=== NIfTI File Processor ===");
    
    // Get file path from command line arguments or use default
    let args: Vec<String> = env::args().collect();
    let file_path = if args.len() > 1 {
        &args[1]
    } else {
        "data/avg152T1.nii"
    };
    
    // Check if file exists
    if !Path::new(file_path).exists() {
        println!("Warning: File '{}' not found. Please provide a valid NIfTI file.", file_path);
        println!("Usage: ./nifti-example [path/to/file.nii]");
        return Ok(());
    }
    
    // Read the NIfTI file with error handling
    let obj = ReaderOptions::new().read_file(file_path)?;
    
    // Access header information
    let header = obj.header();
    //let affine = obj.affine();
    
    // Print basic file information
    println!("NIfTI File: {}", file_path);
    println!("----------------------------------------");
    
    // Print dimensions
    let dims = header.dim()?;
    println!("Dimensions: {:?}", dims);
    println!("Dimensions: {} x {} x {}", dims[0], dims[1], dims[2]);
    // Print data type
    let data_type = header.data_type()?;
    println!("Data type: {:?}", data_type);
    
    // Print voxel dimensions
    let pixdim = &header.pixdim;
    if pixdim.len() >= 4 {
        println!("Voxel dimensions: {:?} mm", &pixdim[1..4]);
    }
    
    // Print other metadata
    println!("Intent: {:?}", header.intent());
    println!("Slice order: {:?}", header.slice_order());
    println!("Slice end: {:?}", header.slice_end);
    println!("Units: {:?}", header.xyzt_units);
    println!("Slope: {:?}", header.scl_slope);
    println!("Intercept: {:?}", header.scl_inter);
    println!("Endianness: {:?}", header.endianness);

    // Access volume information
    let volume = obj.volume();
    println!("Volume dimensions: {:?}", volume.dim());
    
    // Additional information
    println!("Calibration: ({}, {})", header.cal_min, header.cal_max);
    println!("Voxel offset: {}", header.vox_offset);

    use nifti::IntoNdArray;
    let volume = obj.into_volume().into_ndarray::<f32>()?;
    println!("Volume shape: {:?}", volume.shape());
    println!("First voxel value: {}", volume[[0; 3]]);

    use ndarray_stats::QuantileExt;

    // Direct statistical methods (similar to NumPy)
    println!("Min voxel value: {}", volume.min().unwrap());
    println!("Max voxel value: {}", volume.max().unwrap());
    println!("Mean voxel value: {}", volume.mean().unwrap());

    // Additional NumPy-like statistics available:
    println!("Standard deviation: {}", volume.std(0.0)); // ddof=0 like NumPy default
    println!("Variance: {}", volume.var(0.0));


    //println!("Min voxel value: {}", volume.iter().cloned().fold(f32::INFINITY, f32::min));
    //println!("Max voxel value: {}", volume.iter().cloned().fold(f32::NEG_INFINITY, f32::max));
    //println!("Mean voxel value: {}", volume.iter().cloned().sum::<f32>() / volume.len() as f32);
    //println!("Std voxel value: {}", volume.iter.cloned())
    //for (i, &val) in volume.iter().enumerate().take(10) {
    //    println!("Voxel[{}]: {}", i, val);
    //}
    
    // Data type specific information
    match data_type {
        NiftiType::Uint8 => println!("Data type: 8-bit unsigned integer"),
        NiftiType::Int16 => println!("Data type: 16-bit signed integer"),
        NiftiType::Int32 => println!("Data type: 32-bit signed integer"),
        NiftiType::Float32 => println!("Data type: 32-bit floating point"),
        NiftiType::Float64 => println!("Data type: 64-bit floating point"),
        _ => println!("Data type: Other"),
    }
    
    println!("----------------------------------------");
    println!("Successfully read NIfTI file and displayed metadata.");
    
    Ok(())
} 

