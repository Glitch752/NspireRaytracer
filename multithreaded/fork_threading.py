import subprocess
from rt_camera import *
import os

# Fork
child_processes = os.cpu_count()
print(f"Creating {child_processes} child processes")

children = []

for i in range(child_processes):
    start_scanline = i * camera.image_height // child_processes
    end_scanline = (i + 1) * camera.image_height // child_processes
    scanlines = end_scanline - start_scanline

    process = subprocess.Popen(["pypy", "ray_tracer.py", str(start_scanline), str(scanlines), str(i)])
    children.append({
        "process": process,
        "scanline_start": start_scanline,
        "scanlines": scanlines
    })

# Wait for the children to finish
for child in children:
    child["process"].wait()

# Merge the images
final_image = Image.new('RGB', (camera.image_width, camera.image_height))

total_scanlines = 0
for i in range(child_processes):
    print(f"Combining image {i + 1} of {child_processes}")

    image = Image.open(f"output-{i}.png")

    # Shift the image up by the thread's starting scanline and change the height to the number of scanlines
    thread_image = image.crop((0, children[i]["scanline_start"], camera.image_width, children[i]["scanline_start"] + children[i]["scanlines"]))
    final_image.paste(thread_image, (0, total_scanlines))
    total_scanlines += children[i]["scanlines"]

final_image.save("output_threaded_fork.png")