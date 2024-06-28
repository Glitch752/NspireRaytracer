from rt_vec3 import *
from rt_interval import *

class hit_record:
  def __init__(self):
    self.point = point3(0,0,0)
    self.normal = vec3(0,0,0)
    self.t = 0
    self.front_face = False
  def set_face_normal(self, r, outward_normal):
    # outward_normal should be normalized.
    self.front_face = r.direction.dot(outward_normal) < 0
    self.normal = outward_normal if self.front_face else -outward_normal
  def copy_from(self, other):
    self.point = other.point
    self.normal = other.normal
    self.t = other.t
    self.front_face = other.front_face

class hittable:
  def hit(self, r, ray_t, rec):
    return

class hittable_list(hittable):
  def __init__(self):
    self.objects = []
  def add(self, object):
    self.objects.append(object)
  def clear(self):
    self.objects = []
  def hit(self, r, ray_t, rec):
    temp_rec = hit_record()
    hit_any = False
    closest_so_far = ray_t.max
    
    for object in self.objects:
      if object.hit(r, interval.between(ray_t.min, closest_so_far), temp_rec):
        hit_any = True
        closest_so_far = temp_rec.t
    
    rec.copy_from(temp_rec)
    
    return hit_any

class sphere(hittable):
  def __init__(self, center, radius):
    self.radius = radius # Number
    self.center = center # Point
  def hit(self, r, ray_t, rec):
    oc = self.center - r.origin
    a = r.direction.length_squared()
    h = r.direction.dot(oc)
    c = oc.length_squared() - self.radius*self.radius
    discriminant = h*h - a*c
    if discriminant < 0:
      return False
    sqrtd = sqrt(discriminant)
    root = (h - sqrtd) / a
    
    # Find the nearest root that lies in the acceptable range
    if not ray_t.surrounds(root):
      root = (h + sqrtd) / a
      if not ray_t.surrounds(root):
        return False
    
    rec.t = root
    rec.p = r.at(root)
    outward_normal =(rec.p - self.center) / self.radius
    rec.set_face_normal(r, outward_normal)
    
    return True