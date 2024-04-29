from settings import *
import random
from random import randrange as rnd
import pygame.gfxdraw as gfx

class ViewRenderer:
    def __init__(self, engine):
        self.palette = engine.wad_data.asset_data.palette
        self.sprites = engine.wad_data.asset_data.sprites
        self.screen = engine.screen
        self.colors = {}

    def draw_sprite(self):
        img = self.sprites['SHTGA0']
        pos = (H_WIDTH - img.get_width() // 2, HEIGHT - img.get_height())
        self.screen.blit(img,pos)

    def get_color(self, tex, light_level):
        str_light = str(light_level)
        if tex + str_light not in self.colors:
            tex_id = hash(tex)
            random.seed(tex_id)
            color = self.palette[rnd(0, 256)]
            color = color[0] * light_level, color[1] * light_level, color[2] * light_level
            self.colors[tex + str_light] = color
        return self.colors[tex + str_light]

    def draw_vline(self, x, y1, y2, tex, light):
        if y1 < y2:
            gfx.vline(self.screen, x, y1, y2, self.get_color(tex, light))
