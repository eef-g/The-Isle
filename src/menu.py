import pygame as pg

from button_obj import Button

class Menu:
    def __init__(self, engine) -> None:
        # Make sure that the font module is initiated
        pg.font.init()
        # Inherited variables
        self.engine = engine
        self.height = engine.screen.get_height()
        self.width = engine.screen.get_width()
        # Variables for menu customization
        self.font = pg.font.Font("src/resources/font.ttf")
        self.bg_color = (0, 0, 0)
        self.button_color_inactive = (255, 255, 255)
        self.button_color_active = (170, 170, 170)
        self.text_color = (255, 255, 255)

        # Button Variables
        self.button_height = 40
        self.button_width = 140
        self.button_gap = 20

        # Start Button
        self.start_x = self.width / 4
        self.start_y = self.height / 3
        self.start_text = "Start"
        self.start_button = Button(None, (self.start_x, self.start_y), 
                                   "Start", self.font, self.button_color_inactive, 
                                   self.button_color_active, self.start_func)
        # Options Button
        self.option_x = self.start_x
        self.option_y = self.start_y + self.button_height + self.button_gap
        self.option_active = False
        self.option_button = Button(None, (self.option_x, self.option_y),
                                    "Change Map", self.font, self.button_color_inactive,
                                    self.button_color_active, self.option_func)
        # Quit Button
        self.quit_x = self.start_x
        self.quit_y = self.option_y + self.button_height + self.button_gap
        self.quit_active = False
        self.quit_text = "Quit"
        self.quit_button = Button(None, (self.quit_x, self.quit_y), 
                                  "Quit", self.font, self.button_color_inactive, 
                                  self.button_color_active, self.quit_func)

        # All buttons
        self.buttons = [self.start_button, self.option_button, self.quit_button]

    def update(self):
        mouse = pg.mouse.get_pos()
        mouse = (mouse[0], mouse[1])
        for button in self.buttons:
            button.update(self.engine.screen)
            button.changeColor(mouse)

    def start_func(self):
        self.engine.init_game()
        self.engine.current_active = "GAME"

    def option_func(self):
        self.engine.level_index +=1
        if self.engine.level_index > 8:
            self.engine.level_index = 1

    def quit_func(self):
        self.engine.quit()
