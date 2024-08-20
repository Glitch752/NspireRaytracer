use std::convert::TryFrom;

fn fix_image() {
    // Load the image from test.png
    let mut img = image::open("test.png").unwrap();

    let color_array = img.as_mut_rgb8().unwrap();
    // Swap the red and blue channels
    for pixel in color_array.pixels_mut() {
        let r = pixel[0];
        pixel[0] = pixel[2];
        pixel[2] = r;
    }

    // Save the image to test.png
    img.save("test_fixed.png").unwrap();
}

fn main() {
    // Temporary
    // fix_image();
    // return;

    println!(
        "{:?}",
        rusb::devices()
            .unwrap()
            .iter()
            .map(|d| d.device_descriptor().unwrap())
            .filter(|d| d.vendor_id() == 0x0451)
            .collect::<Vec<_>>()
    );

    // 0xe012
    let dev = rusb::open_device_with_vid_pid(0x0451, 0xE022).unwrap();

    println!("USB link speed: {:?}", dev.device().speed());

    let handle = libnspire::Handle::new(dev).unwrap();

    // println!("Device info");
    // dbg!(handle.info());
    // println!("root directory files");
    // dbg!(handle.list_dir("/"));

    println!("Taking screenshot");
    let screenshot = handle.screenshot().unwrap();
    println!("Saving screenshot");
    dbg!(image::DynamicImage::try_from(screenshot)
        .unwrap()
        .save("test.png"));
    fix_image();
}
