import pygame as pg 
from utils.Point import Point3D, Point2D 
from constants import VIEWPORT_RESOLUTION

if __name__ == "__main__":
    pg.init() 
    
    window = pg.display.set_mode(VIEWPORT_RESOLUTION)
    window.fill((255, 255, 255))
    pg.display.update()

    Q = Point3D(300, 300, 0)
    V = Point2D(*VIEWPORT_RESOLUTION) * 0.5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
