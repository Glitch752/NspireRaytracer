from random import *
from rt_interval import *
from rt_vec3 import *
from rt_utils import *
from rt_ray import *
from PIL import Image
from rt_hittables import *

def linear_to_gamma(col):
  return color(
    sqrt(col.x),
    sqrt(col.y),
    sqrt(col.z)
  )

class camera:
  # screen_width = get_screen_dim()[0]
  # screen_height = get_screen_dim()[1]
  
  image_width = 1920
  image_height = 1080
  # image_width = floor(screen_width / 6)
  # image_height = floor(screen_height / 6)
  
  samples_per_pixel = 500
  max_bounce_depth = 50
  
  vfov = 20
  u = vec3(0,0,0)
  v = vec3(0,0,0)
  w = vec3(0,0,0)
  
  lookfrom = point3(13,2,3)
  lookat = point3(0,0,0)
  vup = vec3(0,1,0)
  
  defocus_angle = 0.6 # variation through each pixel
  focus_dist = 10
  
  def __init__(self):
    # To center and make the image fill the screen
    # screen_aspect_w2h = self.screen_width / self.screen_height
    image_aspect_w2h = self.image_width / self.image_height
    
    # self.pixel_offset_x = 0
    # self.pixel_offset_y = 0
    # self.pixel_size = 0
    # if screen_aspect_w2h > image_aspect_w2h:
    #   # Constrained by height
    #   self.pixel_size = \
    #     self.screen_height / self.image_height
    #   self.pixel_offset_x = \
    #     (self.screen_width - self.pixel_size * \
    #     self.image_width) / 2
    # else:
    #   # Constrained by width
    #   self.pixel_size = \
    #     self.screen_width / self.image_width
    #   self.pixel_offset_y = \
    #     (self.screen_height - self.pixel_size * \
    #     self.image_height) / 2
    
    self.center = self.lookfrom
    
    # Camera constants
    # focal_length = (self.lookfrom - self.lookat).length()
    theta = deg2rad(self.vfov)
    h = tan(theta/2)
    viewport_height = 2 * h * self.focus_dist #focal_length
    viewport_width = viewport_height * image_aspect_w2h
    
    # Basis vectors
    self.w.copy_from((self.lookfrom - self.lookat).normalize())
    self.u.copy_from(self.vup.cross(self.w))
    self.v.copy_from(self.w.cross(self.u))
    
    # Viewport edge vectors
    viewport_u = viewport_width * self.u
    viewport_v = viewport_height * -self.v
    # Per-pixel viewport deltas
    self.pixel_delta_u = \
      viewport_u / self.image_width
    self.pixel_delta_v = \
      viewport_v / self.image_height
    
    # Upper-left pixel location
    #self.center - (focal_length*self.w) - \
    viewport_upper_left = \
      self.center - (self.focus_dist*self.w) - \
      viewport_u / 2 - viewport_v / 2
    self.pixel00_location = \
      viewport_upper_left + 0.5 * \
      (self.pixel_delta_u + self.pixel_delta_v)
    
    defocus_radius = self.focus_dist * \
      tan(deg2rad(self.defocus_angle / 2))
    self.defocus_disk_u = self.u * defocus_radius
    self.defocus_disk_v = self.v * defocus_radius
    
    self.pixel_sample_scale = 1 / self.samples_per_pixel

    self.image = Image.new("RGB", (self.image_width, self.image_height), "black")
    self.pixels = self.image.load()
  
  def sample_offset(self):
    return vec3(random() - 0.5, random() - 0.5, 0)
  
  def get_ray(self, x, y):
    offset = self.sample_offset()
    pixel_sample = self.pixel00_location + \
      ((x + offset.x) * self.pixel_delta_u) + \
      ((y + offset.y) * self.pixel_delta_v)
    ray_origin = self.center if self.defocus_angle <= 0 else self.defocus_disk_sample()
    ray_direction = pixel_sample - ray_origin
    return ray(ray_origin, ray_direction)
  
  def defocus_disk_sample(self):
    p = vec3.rand_unit_disk()
    return self.center + \
      (p.x * self.defocus_disk_u) + \
      (p.y * self.defocus_disk_v)
  
  def render(self, world, scanline_start, scanlines):
    self.scanline_start = scanline_start
    self.scanlines = scanlines
    # for y in range(self.image_height):
    progress_bar_length = 40
    for y in range(scanline_start, scanline_start + scanlines):
      print(f"Scanlines remaining: {scanline_start + scanlines - y} [{'=' * floor(progress_bar_length * (y - scanline_start) / scanlines)}{' ' * (progress_bar_length - floor(progress_bar_length * (y - scanline_start) / scanlines))}] {floor(100 * (y - scanline_start) / scanlines)}%")
      for x in range(self.image_width):
        pixel_color = color(0, 0, 0)
        for sample in range(self.samples_per_pixel):
          r = self.get_ray(x, y)
          pixel_color += self.ray_color(
            r,
            self.max_bounce_depth,
            world
          )
        pixel_color *= self.pixel_sample_scale
        pixel_color = linear_to_gamma(pixel_color)
        # set_color(
        #   floor(pixel_color.x * 255),
        #   floor(pixel_color.y * 255),
        #   floor(pixel_color.z * 255)
        # )
        # fill_rect(
        #   x * self.pixel_size + self.pixel_offset_x,
        #   y * self.pixel_size + self.pixel_offset_y,
        #   self.pixel_size,
        #   self.pixel_size
        # )
        self.pixels[x, y] = (
          floor(pixel_color.x * 255),
          floor(pixel_color.y * 255),
          floor(pixel_color.z * 255)
        )
  
  # The pixel color. This is essentially the fragment shader in GPU-terms.
  def ray_color(self, r, depth, world):
    if depth <= 0:
      return color(1, 0.5, 0.2)
    
    rec = hit_record()
    if world.hit(r, interval.between(0.001, infinity), rec):
      #if fabs((rec.point - self.center).length() - self.focus_dist) < 0.1:
      #  return color(1,0,0)
      scattered = ray(rec.point, rec.normal)
      attenuation = color(0, 0, 0)
      if rec.material.scatter(r, rec, attenuation, scattered):
        return attenuation * self.ray_color(scattered, depth-1, world)
      return color(0, 0, 0)
    
    unit_dir = r.direction.normalize()
    a = 0.5 * (unit_dir.y + 1.0)
    return (1-a)*color(1,1,1) + a*color(0.5,0.7,1)