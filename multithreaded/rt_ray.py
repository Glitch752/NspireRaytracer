class ray:
  def __init__(self, origin, direction):
    self.origin = origin # point
    self.direction = direction # vec3
  def at(self, time):
    return self.origin + self.direction * time