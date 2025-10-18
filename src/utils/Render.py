from utils.Camera import Camera 
from utils.Polygon import Polygon, Polygon2D, Polygon3D, Face
from utils.Point import Point3D
import pygame as pg 
from pygame import gfxdraw

class Render:
    def __init__(self, camera: Camera, surface: pg.Surface):
        self.camera = camera
        self.surface = surface 


    def draw_polygon(self, poly: Polygon):
        if isinstance(poly, Polygon2D):
            vertices_tuple = poly.vertices_to_tuple()
        elif isinstance(poly, Face):
            vertices_tuple = tuple(map(lambda p: p.to_2D().coords, poly.vertices))
        elif isinstance(poly, Polygon3D):
            for face in poly.faces:
                self.draw_polygon(face)
            return
        
        gfxdraw.aapolygon(self.surface, vertices_tuple, poly.color)
        gfxdraw.filled_polygon(self.surface, vertices_tuple, poly.color)