import pygame as pg 
from pygame import gfxdraw
from utils.Camera import Camera
from utils.Point import Point3D, Point2D 
from utils.Polygon import Face
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

    tl = Point3D(300, 600, 40)
    bl = Point3D(tl.x-100, tl.y+50, 40)
    tr = Point3D(tl.x+100, tl.y+50, 40)
    br = Point3D(tl.x, tl.y+100, tl.z)

    render = Render(Camera(1, 2, 3, 4, 5), window)
    poly = Face([tl, bl, br, tr])
    i = 0
    j = 180

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        render.draw_polygon(poly)

        tr.setx(300 + 100*math.cos(math.radians(i)))
        tr.setz(40 + 40*math.sin(math.radians(i)))

        bl.setx(300 + 100*math.cos(math.radians(j)))
        bl.setz(40 + 40*math.sin(math.radians(j)))

        i += 0.1
        j += 0.1

        i = i % 360
        j = j % 360

        pg.display.update()
        window.fill((255, 255, 255))
