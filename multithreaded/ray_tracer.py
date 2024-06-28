from math import *
from rt_interval import *
from rt_vec3 import *
from rt_utils import *
from rt_ray import *
from rt_hittables import *
from rt_camera import *
from rt_material import *
from sys import argv
from random import uniform, random, seed

process_args = argv[1:]

world = hittable_list()

seed(0)

ground_material = lambertian(color(0.5, 0.5, 0.5))
world.add(sphere(point3(0,-1000,0), 1000, ground_material))

for a in range(-11, 11):
  for b in range(-11, 11):
    choose_mat = random()
    center = point3(a + 0.9 * random(), 0.2, b + 0.9 * random())

    if (center - point3(4, 0.2, 0)).length() > 0.9:
      if choose_mat < 0.8:
        # diffuse
        albedo = color.random() * color.random()
        sphere_material = lambertian(albedo)
        world.add(sphere(center, 0.2, sphere_material))
      elif choose_mat < 0.95:
        # metal
        albedo = color(uniform(0.5, 1), uniform(0.5, 1), uniform(0.5, 1))
        fuzz = uniform(0, 0.5)
        sphere_material = metal(albedo, fuzz)
        world.add(sphere(center, 0.2, sphere_material))
      else:
        # glass
        sphere_material = dielectric(1.5)
        world.add(sphere(center, 0.2, sphere_material))

material1 = dielectric(1.5)
world.add(sphere(point3(0, 1, 0), 1.0, material1))

material2 = lambertian(color(0.4, 0.2, 0.1))
world.add(sphere(point3(-4, 1, 0), 1.0, material2))

material3 = metal(color(0.7, 0.6, 0.5), 0.0)
world.add(sphere(point3(4, 1, 0), 1.0, material3))

cam = camera()
cam.render(world, int(process_args[0]), int(process_args[1]))

cam.image.save(f"output-{process_args[2]}.png")

print(f"Thread {process_args[2]} finished ================================================================================================")