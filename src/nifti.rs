extern crate nifti;

use nifti::NiftiImage;
use nifti::NiftiObject;
use nifti::ReaderOptions;

fn main() {
    
    let nifti = NiftiObject::from_file("data/dwi.nii.gz", ReaderOptions::default()).unwrap();
    let volume = nifti.into_volume();
    println!("Hello, world!");
} 

