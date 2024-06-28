from rt_hittables import *
from random import *

class material:
  def scatter(r_in, rec, attenuation, scattered):
    return False

class lambertian(material):
  def __init__(self, albedo):
    self.albedo = albedo
   
  def scatter(self, r_in, rec, attenuation, scattered):
    dir = rec.normal + vec3.rand_normalized()
    
    # Catch problematic scatter direction
    if dir.near_zero():
      dir = rec.normal
    
    scattered.origin = rec.point
    scattered.direction = dir
    attenuation.copy_from(self.albedo)
    return True


class metal(material):
  def __init__(self, albedo, fuzz):
    self.albedo = albedo
    self.fuzz = fuzz
   
  def scatter(self, r_in, rec, attenuation, scattered):
    dir = r_in.direction.reflect(rec.normal)
    dir = dir.normalize() + (self.fuzz * vec3.rand_normalized())
    
    scattered.origin = rec.point
    scattered.direction = dir
    attenuation.copy_from(self.albedo)
    return scattered.direction.dot(rec.normal) >0

class dielectric(material):
  def __init__(self, ior):
    self.ior = ior
  
  def scatter(self, r_in, rec, attenuation, scattered):
    attenuation.copy_from(color(1, 1, 1))
    ri = (1 / self.ior) if rec.front_face else self.ior
    
    norm_dir = r_in.direction.normalize()
    cos_theta = min((-norm_dir).dot(rec.normal), 1.0)
    sin_theta = sqrt(1 - cos_theta*cos_theta)
    
    direction = vec3(0, 0, 0)
    
    if ri * sin_theta >1.0 or self.reflectance(cos_theta, ri) > random():
      direction.copy_from(norm_dir.reflect(rec.normal))
    else:
      direction.copy_from(norm_dir.refract(rec.normal, ri))
    
    scattered.origin = rec.point
    scattered.direction = direction
    
    return True
  
  def reflectance(self, cosine, ior):
    r0 = (1-ior) / (1+ior)
    r0 = r0*r0
    return r0 +(1-r0)*pow(1-cosine,5)