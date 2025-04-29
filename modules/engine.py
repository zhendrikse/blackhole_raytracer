from modules.color import Color
import numpy as np
from PIL import Image

class Engine:
  def __init__(self, scene, n_iter=200, dt=0.002):
    self.output = None
    self.scene = scene
    self.n_iter = n_iter
    self.dt = dt

  def render(self):
    ratio = float(self.scene.width)/self.scene.height
    x0, x1 = -1.0, 1.0
    y0, y1 = -1.0/ratio, 1.0/ratio
    xstep, ystep = (x1-x0)/(self.scene.width-1), (y1-y0)/(self.scene.height-1)

    for j in range(self.scene.height):
      y = y0 + j*ystep

      if (j+1) % 10 == 0:
        print('line ' + str(j+1) + '/' + str(self.scene.height))

      for i in range(self.scene.width):
        x = x0 + i*xstep
        ray = self.scene.camera.ray(x, y)
        self.scene.image.set_pixel(i, j, self.trace(ray))

    self.output = Image.fromarray(self.scene.image.pixels.astype(np.uint8))

  def trace(self, ray, depth=0):
    color = Color()
    for t in range(self.n_iter):
      r = self.scene.blackhole.position - ray.position
      a = 7.0e-3 * (self.scene.blackhole.mass / r**5) * r.normalize()
      ray.accelerate(a)
      ray.step(t * self.dt)

      ray_bh_dist = (ray.position-self.scene.blackhole.position).norm

      if ray.crossed_xz and ray.cross_point and self.scene.disk.is_in(ray.cross_point):
        color = self.calculate_ray_color(ray)
        break
      elif ray_bh_dist <= self.scene.blackhole.radius:
        break
      elif ray_bh_dist >= 15.0:
        break
    return color

  def save(self, filename):
    self.output.save(filename)

  def calculate_ray_color(self, ray):
    point = ray.cross_point
    distance = (point - self.scene.blackhole.position).norm
    brightness = self.calculate_brightness(distance)

    red = 255
    green = round(255 * brightness * 2) if brightness < 0.5 else 255
    blue = round(255 * (brightness - .5) * 2) if brightness < 0.5 else 0
    return Color((red, green, blue))

  def calculate_brightness(self, distance):
    inner = self.scene.disk.inner_r
    outer = self.scene.disk.outer_r
    brightness = 1.0 - (distance - inner) / (outer - inner)
    brightness = max(0.0, min(1.0, brightness))
    return brightness ** 2.5  # nonlinear falloff
