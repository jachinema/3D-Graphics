from utils.Camera import Camera 
from utils.Polygon import Polygon, Polygon2D, Polygon3D, Face, CompositeShape
from constants import VIEWPORT_RESOLUTION
from utils.Point import Point3D
import pygame as pg 
from pygame import gfxdraw
import math

class Render:
    vanishing_point = Point3D(VIEWPORT_RESOLUTION[0]/2, VIEWPORT_RESOLUTION[1]/2, 0)

    def __init__(self, camera: Camera, surface: pg.Surface):
        self.camera = camera
        self.surface = surface 


    def draw_polygon(self, poly: Polygon):
        if isinstance(poly, Polygon2D):
            vertices_tuple = poly.vertices_to_tuple()
        elif isinstance(poly, Face):
            vertices_tuple = tuple(map(lambda p: p.to_2D().coords, poly.vertices))
        elif isinstance(poly, Polygon3D):
            for face in sorted(poly.faces, key=lambda f: f.center().dist(Render.vanishing_point), reverse=True):
                self.draw_polygon(face)
            return
        elif isinstance(poly, CompositeShape):
            for face in sorted(poly.all_faces, key=lambda f: f.center().dist(Render.vanishing_point), reverse=True):
                self.draw_polygon(face)
            return
        
        gfxdraw.aapolygon(self.surface, vertices_tuple, poly.color)
        gfxdraw.filled_polygon(self.surface, vertices_tuple, poly.color)