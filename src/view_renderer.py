from settings import *
import random
from random import randrange as rnd
import pygame.gfxdraw as gfx

class ViewRenderer:
    def __init__(self, engine):
        self.screen = engine.screen
        self.colors = {}

    def get_color(self, tex, light_level):
        str_light = str(light_level)
        if tex + str_light not in self.colors:
            tex_id = hash(tex)
            l = light_level / 255
            random.seed(tex_id)
            rng = (50, 256)
            color = rnd(*rng) * l, rnd(*rng) * l, rnd(*rng) * l
            self.colors[tex + str_light] = color
        return self.colors[tex + str_light]

    def draw_vline(self, x, y1, y2, tex, light):
        if y1 < y2:
            gfx.vline(self.screen, x, y1, y2, self.get_color(tex, light))

























