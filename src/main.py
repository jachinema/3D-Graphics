import pygame as pg 
from pygame import gfxdraw
from utils.Camera import Camera
from utils.Point import Point3D, Point2D
from utils.Polygon import Face, Cube, CompositeShape
from utils.Render import Render
from constants import VIEWPORT_RESOLUTION
import math

if __name__ == "__main__":
    pg.init() 
    
    window = pg.display.set_mode(VIEWPORT_RESOLUTION)
    window.fill((255, 255, 255))
    pg.display.update()

    render = Render(Camera(1, 2, 3, 4, 5), window)
    poly = Cube(Point3D(300, 300, 0), 100)
    poly2 = Cube(Point3D(450, 300, 0), 100)

    construct = CompositeShape([poly, poly2])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        render.draw_polygon(construct)

        x, y = pg.mouse.get_pos()

        poly = Cube(Point3D(x, y, 0), 100)
        poly2 = Cube(Point3D(x+150, y, 0), 100)
        construct = CompositeShape([poly, poly2])

        pg.display.update()
        window.fill((255, 255, 255))
 