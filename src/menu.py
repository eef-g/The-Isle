import pygame as pg

class Menu:
    def __init__(self, engine) -> None:
        # Make sure that the font module is initiated
        pg.font.init()
        # Inherited variables
        self.engine = engine
        self.height = engine.screen.get_height()
        self.width = engine.screen.get_width()
        # Variables for menu customization
        # TODO: Change from system font to the raylib font
        self.font = pg.font.SysFont("Corbel", 35)
        self.bg_color = (0, 0, 0)
        self.button_color_inactive = (100, 100, 100)
        self.button_color_active = (170, 170, 170)
        self.text_color = (255, 255, 255)
        # Button Variables
        self.button_height = 40
        self.button_width = 140
        self.button_gap = 20
        # Start Button
        self.start_x = self.width / 4
        self.start_y = self.height / 3
        self.start_active = False
        self.start_text = "Start"
        # Options Button
        self.option_x = self.start_x
        self.option_y = self.start_y + self.button_height + self.button_gap
        self.option_active = False
        self.option_text = "Options"
        # Quit Button
        self.quit_x = self.start_x
        self.quit_y = self.option_y + self.button_height + self.button_gap
        self.quit_active = False
        self.quit_text = "Quit"

    def update(self):
        mouse = pg.mouse.get_pos()
        mouse = (mouse[0], mouse[1])
        # Start Button
        self.start_active = self.mouse_check(mouse, self.start_x, self.start_y)
        # Options Button
        self.option_active = self.mouse_check(mouse, self.option_x, self.option_y)
        # Quit Button
        self.quit_active = self.mouse_check(mouse, self.quit_x, self.quit_y)
        self.get_updates()
    
    def get_updates(self):
        for e in pg.event.get():
            if e.type == pg.MOUSEBUTTONUP:
                if self.start_active:
                    self.start_func
                if self.option_active:
                    self.option_func
                if self.quit_active:
                    self.quit_func


    def mouse_check(self, mouse_pos, start_x, start_y):
        x_bool = start_x <= mouse_pos[0] <= start_x + self.button_width
        y_bool = start_y <= mouse_pos[1] <= start_y + self.button_height
        return x_bool and y_bool

    def draw(self):
        # Draw Start button
        self.draw_button(self.start_active, self.start_x, self.start_y, self.start_text)
        # Draw Options button
        self.draw_button(self.option_active, self.option_x, self.option_y, self.option_text)
        # Draw Quit Button
        self.draw_button(self.quit_active, self.quit_x, self.quit_y, self.quit_text)
        
    def draw_button(self, active, button_x, button_y, txt):
        button_color = None
        if active:
            button_color = self.button_color_active
        else:
            button_color = self.button_color_inactive
        pg.draw.rect(self.engine.screen, button_color, [button_x, button_y, self.button_width, self.button_height])
        rendered_txt = self.font.render(txt, False, self.text_color)
        self.engine.screen.blit(rendered_txt, (button_x, button_y))


    def start_func(self):
        print("Start Function")

    def option_func(self):
        print("Option Function")

    def quit_func(self):
        print("Quit Function")
