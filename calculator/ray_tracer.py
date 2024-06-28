from math import *
from rt_interval import *
from rt_vec3 import *
from rt_utils import *
from rt_ray import *
from rt_hittables import *
from rt_camera import *
from rt_material import *

# World
world = hittable_list()

mat_ground = lambertian(color(0.8, 0.8, 0.0))
mat_center = lambertian(color(0.1, 0.2, 0.5))
mat_left = dielectric(1.5)
mat_bubble = dielectric(1 / 1.5)
mat_right = metal(color(0.8, 0.6, 0.2), 0)

world.add(sphere(point3(0,-100.5,-1), 100, mat_ground))
world.add(sphere(point3(0,0,-1.2), 0.5, mat_center))
world.add(sphere(point3(-1,0,-1), 0.5, mat_left))
world.add(sphere(point3(-1,0,-1), 0.4, mat_bubble))
world.add(sphere(point3(1,0,-1), 0.5, mat_right))

cam = camera()
cam.render(world)