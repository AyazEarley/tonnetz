import pygame
import settings
from options import Button

def lerp_color(color_a, color_b, t):
    return tuple(a + (b - a) * t for a, b in zip(color_a, color_b))
FADE_SPEED = 8  # progress units per second

def render_multiline(font, text, color, line_spacing=5):
    lines = text.split("\n")
    surfaces = [font.render(line, True, color) for line in lines]
    return surfaces, line_spacing

class HowToPlay:
    def __init__(self, screen):
        self.screen = screen
        self.next_state = None

        width = screen.get_width()

        self.titleFont = pygame.font.SysFont("corbel", 84)
        self.scoreFont = pygame.font.SysFont("corbel", 20)
        self.buttonFont = pygame.font.SysFont("corbel", 48)

        NORMAL = (255, 255, 255)

        if settings.P1COLOR == (255, 0, 255):
            p1ColorText = "magenta"
        elif settings.P1COLOR == (255, 255, 0):
            p1ColorText = "yellow"
        else:
            p1ColorText = "cyan"

        if settings.P2COLOR == (255, 0, 255):
            p2ColorText = "magenta"
        elif settings.P2COLOR == (255, 255, 0):
            p2ColorText = "yellow"
        else:
            p2ColorText = "cyan"

        self.buttons = [

            Button("Back to Menu", self.buttonFont, (width // 2, 550), NORMAL, (100, 100, 100), "menu"),
            
        ]
        self.button_by_action = {b.action: b for b in self.buttons}

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                self.handle_click(button)

    def handle_click(self, button):
        
        if button.action == "menu":
            self.next_state ="menu"
            settings.save_settings()
            

        

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(dt, mouse_pos)

    def draw(self):
        self.screen.fill((21, 21, 21))

        titleSurface = self.titleFont.render("How to Play", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(self.screen.get_width() // 2, 75))
        self.screen.blit(titleSurface, titleRect)

        lines, spacing = render_multiline(self.scoreFont, "Tonnetz is a strategy game I created, inspired by my background in music\ntheory. The game is played on a lattice of musical pitches, called The Tonnetz.\nTwo players  take turns capturing pitches on the board in an attempt to create\nharmonies and earn points. No music theory experience is required to play.\n\nOn your turn, you can capture any pitch adjacent to one you already control. You\ncan also capture pitches who share a name with one you already control. Your\noptions will be highlighted on your turn, and you can click on one to capture it. If you\ncapture three pitches that form a triangle, this will create a harmony and you get a\npoint. If you have no available moves, your turn will instantly end. When all\npitches are captured, the player with the most harmonies wins. In the event of a\ntie, player 2 wins, because player 1 went first. \n\nLastly, I hope you enjoy the soundtrack :)", (255, 255, 255))

        LEFT_MARGIN = 80  # distance from the left edge of the screen
        y = 150
        for line_surface in lines:
            line_rect = line_surface.get_rect(topleft=(LEFT_MARGIN, y))
            self.screen.blit(line_surface, line_rect)
            y += line_surface.get_height() + spacing

        for button in self.buttons:
            button.draw(self.screen)