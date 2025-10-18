import pygame as pg 
from pygame import gfxdraw
from utils.Camera import Camera
from utils.Point import Point3D, Point2D
from utils.Polygon import Face, Cube
from utils.Render import Render
from constants import VIEWPORT_RESOLUTION
import math


def draw_point(window, point):
    pg.draw.circle(window, (0, 0, 255), point.coords[:2], 15)

if __name__ == "__main__":
    pg.init() 
    
    window = pg.display.set_mode(VIEWPORT_RESOLUTION)
    window.fill((255, 255, 255))
    pg.display.update()

    # tl = Point3D(300, 600, 40)
    # bl = Point3D(tl.x-100, tl.y+50, 40)
    # tr = Point3D(tl.x+100, tl.y+50, 40)
    # br = Point3D(tl.x, tl.y+100, tl.z)

    render = Render(Camera(1, 2, 3, 4, 5), window)
    poly = Cube(Point3D(300, 300, 0), 100)
    i = 0
    j = 180
    k = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        render.draw_polygon(poly)
        poly = Cube(Point3D(*pg.mouse.get_pos(), 0), 100)


        pg.display.update()
        window.fill((255, 255, 255))
