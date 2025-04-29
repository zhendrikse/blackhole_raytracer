from modules.vector import Vector
from modules.ray import Ray

class Camera:
  def __init__(self, origin, direction, focal_length):
    self.origin = origin
    self.direction = direction.normalize()
    self.focal_length = focal_length
    self.normal = self.origin + self.focal_length*self.direction
    self.right = Vector(1, 0, 0)
    self.up = self.normal.cross(self.right).normalize()
    self.rotate_z()

  def rotate_z(self, angle=20):
    self.right = self.right.rotate_z(angle)
    self.up = self.up.rotate_z(angle)

  def ray(self, x, y):
    point = self.normal + x*self.right + y*self.up
    return Ray(self.origin, point - self.origin)