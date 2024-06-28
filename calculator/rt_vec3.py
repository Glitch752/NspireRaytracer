from math import *
from random import *

class vec3:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
  def __str__(self):
    return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"
  # Inequalities are unnecessary, but for reference are dunder lt, le, eq, ne, gt, and ge.
  def __len__(self):
    return self.len()
  def __add__(self, other): # vec1 + vcc2
    return vec3(self.x + other.x, self.y + other.y, self.z + other.z)
  def __sub__(self, other): # vec1 - vec2
    return vec3(self.x - other.x, self.y - other.y, self.z - other.z)
  def __mul__(self, other): # vec1 * vec2
    if isinstance(other, (int, float)):
      return self.mul_all(other)
    return vec3(self.x * other.x, self.y * other.y, self.z * other.z)
  def __rmul__(self, other): # num * vec1
    return self.__mul__(other)
  def __truediv__(self, other): # vec1 / vec2
    if isinstance(other, (int, float)):
      return self.div_all(other)
    return vec3(self.x / other.x, self.y / other.y, self.z / other.z)
  def __rtruediv__(self, other): # num / vec1
    return self.__truediv__(other)
  # vec1 // vec2: __floordiv__
  # vec1 @ vec2: __matmul__
  # vec1 % vec2: __mod__
  # divmod(vec1, vec2): __divmod__
  # pow(vec1, vec2[, modulo]), vec1 ** vec2: __pow__
  # vec1 << vec2: __lshift__
  # vec1 >> vec2: __rshift__
  # vec1 & vec2: __and__
  # vec1 ^ vec2: __xor__
  # vec1 | vec2: __or__
  # Some swapped versions (e.g. __radd__) not needed
  # Assignment versions (e.g. __iadd__) not implemented explicitly but work
  def __neg__(self): # -vec
    return vec3(-self.x, -self.y, -self.z)
  # +vec: __pos__
  def __abs__(self): # abs(vec)
    return vec3(fabs(self.x), fabs(self.y), fabs(self.z))
  # ~vec: __invert__
  # Casts not implemented: __complex__, __int__, __float__
  # round(vec): __round__
  # trunc(vec): __trunc__
  # floor(vec): __floor__
  # ceil(vec): __ceil__
  
  def mul_all(self, scalar):
    return vec3(self.x * scalar, self.y * scalar, self.z * scalar)
  def div_all(self, scalar):
    return vec3(self.x / scalar, self.y / scalar, self.z / scalar)
  
  def length(self):
    return sqrt(self.length_squared())
  def length_squared(self):
    return self.x*self.x + self.y*self.y + self.z*self.z
  def normalize(self):
    return self / self.length()
  def dot(self, other):
    return self.x*other.x + self.y*other.y + self.z*other.z
  def cross(self, other):
    return vec3(
      self.y * other.z - self.z * other.y,
      self.z * other.x - self.x * other.z,
      self.x * other.y - self.y * other.x
    )
  
  def rand_between(min, max):
    return vec3(
      uniform(min,max),
      uniform(min,max),
      uniform(min,max)
    )
  rand_between = staticmethod(rand_between)
  
  def random():
    return vec3(random(), random(), random())
  random = staticmethod(random)
  
  def rand_unit_sphere():
    while True:
      p = vec3.rand_between(-1, 1)
      if p.length_squared() < 1:
        return p
  rand_unit_sphere = staticmethod(rand_unit_sphere)
  
  def rand_normalized():
    return vec3.rand_unit_sphere().normalize()
  rand_normalized = staticmethod(rand_normalized)
  
  def rand_on_hemisphere(normal):
    unit = vec3.rand_normalized()
    return unit if unit.dot(normal) > 0.0 else -unit
  rand_on_hemisphere = staticmethod(rand_on_hemisphere)
  
  def rand_unit_disk():
    while True:
      p = vec3(uniform(-1,1),uniform(-1,1),0)
      if p.length_squared() < 1:
        return p
    
  
  def near_zero(self):
    s = 0.00000001
    return (fabs(self.x) < s  and fabs(self.y) < s  and fabs(self.z) < s)
  
  def reflect(self, over):
    return self - 2 * self.dot(over) * over
  
  def refract(self, over, etai_over_etat):
    cos_theta = min((-self).dot(over), 1.0)
    r_out_perp = etai_over_etat * (self + cos_theta * over)
    r_out_parallel = -sqrt(fabs(1 - r_out_perp.length_squared())) * over
    return r_out_perp + r_out_parallel
  
  def copy_from(self, other):
    self.x = other.x
    self.y = other.y
    self.z = other.z

point3 = vec3
color = vec3