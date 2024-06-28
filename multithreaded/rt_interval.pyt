from rt_utils import *

class interval:
  def __init__(self):
    self.min = infinity
    self.max = -infinity
  
  def between(min, max):
    int = interval()
    int.min = min
    int.max = max
    return int
  between = staticmethod(between)
  
  def size(self):
    return self.max - self.min
  def contains(self, x):
    return self.min <= x <= self.max
  def surrounds(self, x):
    return self.min < x < self.max

interval.empty = interval()
interval.all = interval.between(-infinity, infinity)
