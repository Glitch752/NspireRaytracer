use std::io::Read;

fn decode_file() {
    let mut file = std::fs::File::open("RayTracer.tns").unwrap();
    let mut buf = vec![];
    file.read_to_end(&mut buf).expect("Could not read file");

    let mut decoder = zstd::Decoder::new(&buf[..]).unwrap();
    let mut decoded = vec![];
    decoder
        .read_to_end(&mut decoded)
        .expect("Could not decode file");

    std::fs::write("RayTracer.tns.decoded", decoded).expect("Failed to save file");
}

fn main() {
    // Temporary
    decode_file();
    return;

    let dev = rusb::open_device_with_vid_pid(0x0451, 0xE022).unwrap();
    println!("USB link speed: {:?}", dev.device().speed());

    let handle = libnspire::Handle::new(dev).unwrap();

    println!("root directory files");
    dbg!(handle.list_dir("/"));

    println!("PyLib directory files");
    dbg!(handle.list_dir("/PyLib"));

    // Download PyLib/RayTracer.tns
    let mut buf = Vec::with_capacity(1024 * 1024); // 1MB (initial capacity)
    let bytes_read = handle
        .read_file("/PyLib/RayTracer.tns", &mut buf, &mut |prog| {
            println!("{}", prog)
        })
        .expect("Failed to download file");

    println!("Read {} bytes", bytes_read);

    println!("Downloaded {} bytes", buf.len());

    std::fs::write("RayTracer.tns", buf.clone()).expect("Failed to save file");

    decode_file();
}
