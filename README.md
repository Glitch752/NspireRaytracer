# TI-NSpire Ray Tracer

This repository includes a variety of directories related to my TI-Nspire ray tracer, which was based on the fantastic book [Ray Tracing in One Weekend](https://raytracing.github.io/) by Peter Shirley and contributors.

## Directory structure
- `calculator/`: The original code written for my TI-Nspire CX II calculator, written in Python, dumped into a `.tns` file and exported.
- `multithreaded/`: After dumping the ray tracer, I converted it to use the python PIL library and implemented multi-process multithreading to speed up the rendering process for large renders on my computer. **This uses the exact same underlying ray tracing logic as the calculator version, but with added multithreading and a different output method.**
- `images/`: Images from all versions of the raytracer used in the samples below. Images are dumped using a modified version of the [`nspire-rs`](https://crates.io/crates/libnspire) crate, since the original crate does not properly work with my calculator. I may upload this as well after some cleanup.

## Samples

### Calculator version
An overnight render with depth-of-field:  
![An overnight render](images/overnight_test_fixed.png)

An older picture with a low sample count and resolution:  
![An older picture with a low sample count and resolution](images/old_picture.png)

An older timelapsed render:  
![An older timelapsed render](images/old_timelapse.mp4)

A timelapse of a progressive render (sorry it's sideways!):  
![A timelapse of a progressive render](images/progressive_render.mp4)

### Multithreaded computer version (using the same raytracer)
A render of the same scene as above, but with a much higher resolution and rendered in a few minutes:  
![A render of the same scene as above, but with a much higher resolution and rendered in a few minutes](images/output_dof.png)

A high-resolution render of the closing picture from Ray Tracing in One Weekend:  
![A high-resolution render of the closing picture from Ray Tracing in One Weekend](images/output_threaded.png)