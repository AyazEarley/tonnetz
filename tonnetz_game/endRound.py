import pygame
from menu import Button
from settings import *
import game

class EndRound:
    def __init__(self, screen, p1_score, p2_score):
        global round1P2Score, round1P1Score, ROUND
        self.screen = screen
        self.next_state = None
        self.p1_score = p1_score
        self.p2_score = p2_score

        game.ROUND = 2
        game.round1P1Score = p1_score
        game.round1P2Score = p2_score

        width = screen.get_width()

        self.titleFont = pygame.font.SysFont("corbel", 84)
        self.scoreFont = pygame.font.SysFont("corbel", 36)
        self.buttonFont = pygame.font.SysFont("corbel", 48)

        NORMAL = (255, 255, 255)

        self.buttons = [
            Button("Play next round", self.buttonFont, (width // 2, 330), NORMAL, (0, 255, 255)),
            Button("Back to Menu", self.buttonFont, (width // 2, 400), NORMAL, (255, 0, 255)),
            Button("Quit to desktop", self.buttonFont, (width // 2, 470), NORMAL, (100, 100, 100)),
        ]

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                self.handle_click(button.text)

    def handle_click(self, button_text):
        if button_text == "Play next round":
            self.next_state = "game"
        elif button_text == "Back to Menu":
            game.ROUND = 1
            game.round1P1Score, game.round1P2Score = 0, 0
            self.next_state = "menu"
        elif button_text == "Quit to desktop":
            pygame.quit()
            raise SystemExit

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(dt, mouse_pos)

    def draw(self):
        self.screen.fill((21, 21, 21))

        title_text = f"Round 1 Complete!"

        titleSurface = self.titleFont.render(title_text, True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(titleSurface, titleRect)

        p1_text = f"Player 1: {self.p1_score}"
        p2_text = f"Player 2: {self.p2_score}"

        p1_surface = self.scoreFont.render(p1_text, True, P1COLOR)
        p2_surface = self.scoreFont.render(p2_text, True, P2COLOR)

        spacing = 40  # gap between the two pieces of text
        total_width = p1_surface.get_width() + spacing + p2_surface.get_width()

        start_x = (self.screen.get_width() - total_width) // 2
        center_y = 230

        p1_rect = p1_surface.get_rect(midleft=(start_x, center_y))
        p2_rect = p2_surface.get_rect(midleft=(p1_rect.right + spacing, center_y))

        self.screen.blit(p1_surface, p1_rect)
        self.screen.blit(p2_surface, p2_rect)

        for button in self.buttons:
            button.draw(self.screen)