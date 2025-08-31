fn main() {
    let brain_data = vec![1, 2, 3, 4, 5];  // Simulating image data
    println!("Original data: {:?}", brain_data);
    
    let result = process_data(&brain_data);
    println!("Result: {}", result);
    
    // Try to use brain_data again
    println!("Brain data after processing: {:?}", brain_data);
    // This will cause a compile-time error because brain_data has been moved

    // Calculate lesion volume
    let lesion_mask = vec![0, 1, 1, 0, 1];  // Simulated binary mask
    let lesion_volume = calculate_lesion_volume(&lesion_mask);
    println!("Lesion volume: {:.3} cc", lesion_volume);
    filter_lesion(&lesion_mask);
}

//fn process_data(mut data: &Vec<i32>) -> i32 {
fn process_data(data: &Vec<i32>) -> i32 {
    //data[0] = 999;  // Modify the data
    data.iter().sum()
}

fn calculate_lesion_volume(mask: &Vec<u8>) -> f32 { 
    mask.iter().filter(|&&v| v > 0).count() as f32 * 0.001  // Example calculation
}

fn filter_lesion(mask: &Vec<u8>)  { 
    let filtered_iterator = mask.iter().filter(|&&v| v > 0);
    println!("Filtered iterator: {:?}", filtered_iterator);

    let collected_values: Vec<_> = mask.iter().filter(|&&v| v > 0).collect();
    println!("Collected values: {:?}", collected_values);

    let enumerated_values: Vec<_> = mask.iter().enumerate().filter(|&(_i, &v)| v > 0).collect();
    println!("Enumerated values: {:?}", enumerated_values);
}

fn calculate_dice_coefficient(mask1: &Vec<u8>, mask2: &Vec<u8>) -> f64 { 
    // Example calculation
    let intersection: usize = mask1.iter().zip(mask2.iter()).filter(|(&a, &b)| a > 0 && b > 0).count();
    let size1: usize = mask1.iter().filter(|&&v| v > 0).count();
    let size2: usize = mask2.iter().filter(|&&v| v > 0).count();
    (2.0 * intersection as f64) / (size1 as f64 + size2 as f64)
 }
