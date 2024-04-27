import pygame as pg
import sys
from settings import *
from data import WADData
from map_renderer import MapRenderer
from player import Player
from bsp import BSP

class Engine:
    def __init__(self, wad_path='src/resources/wads/doom1.wad'):
        self.wad_path = wad_path

        # Window Code
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.running = True
        self.dt = 1/60
        icon = pg.image.load("src/resources/doom_clone.png")
        pg.display.set_icon(icon)
        pg.display.set_caption("Doom")
        # Final Setup
        self.on_init()

    def on_init(self):
        # Model-Based Code
        self.wad_data = WADData(self, map_name='E1M1')
        # Controller-Based Code
        self.player = Player(self)
        self.bsp = BSP(self)
        # View-Based Code
        self.map_renderer = MapRenderer(self)
        self.run()

    def update(self):
        self.player.update()
        self.bsp.update()
        self.dt = self.clock.tick()

    def draw(self):
        # Flip first for debugging -- Uncomment line when building
        pg.display.flip()
        self.screen.fill('black')
        self.map_renderer.draw()
        #pg.display.flip()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    doom = Engine()
