import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import sys
from settings import *
from data import WADData
from map_renderer import MapRenderer
from player import Player
from bsp import BSP
from seg_handler import SegHandler
from view_renderer import ViewRenderer
from menu import Menu

class Engine:
    def __init__(self, wad_path='src/resources/wads/doom1.wad'):
        self.wad_path = wad_path

        # Window Code
        self.screen = pg.display.set_mode(WIN_RES)
        self.framebuffer = pg.surfarray.array3d(self.screen)
        self.clock = pg.time.Clock()
        self.running = True
        self.dt = 1/60
        icon = pg.image.load("src/resources/doom_clone.png")
        pg.display.set_icon(icon)
        self.level_index = 1
        self.menu = Menu(self)
        self.current_active = "MENU"

    def init_game(self):
        map = "E1M" + str(self.level_index)
        self.wad_data = WADData(self, map)
        self.map_renderer = MapRenderer(self)
        self.player = Player(self)
        self.bsp = BSP(self)
        self.seg_handler = SegHandler(self)
        self.view_renderer = ViewRenderer(self)

    def update(self):
        pg.display.set_caption(f"Doom - E1M{self.level_index}")
        if self.current_active == 'MENU':
            self.menu.update()
        if self.current_active == 'GAME':
            self.player.update()
            self.seg_handler.update()
            self.bsp.update()
        self.dt = self.clock.tick()

    def draw(self):
        if self.current_active == 'MENU':
            pass
        elif self.current_active == 'GAME':
            pg.surfarray.blit_array(self.screen, self.framebuffer)
            self.view_renderer.draw_sprite()
        pg.display.flip()

    def check_events(self):
        mouse_pos = pg.mouse.get_pos()
        for e in pg.event.get():
            if e.type == pg.QUIT or pg.key.get_pressed() == pg.key.get_pressed()[pg.K_ESCAPE]:
                self.running = False
                pg.quit()
                sys.exit()

            if e.type == pg.MOUSEBUTTONDOWN:
                if self.current_active == 'MENU':
                    for button in self.menu.buttons:
                        if button.checkForInput(mouse_pos):
                            button.func()

    def quit(self):
        self.running = False
        pg.quit()
        sys.exit()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    doom = Engine()
    doom.run()
