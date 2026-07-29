import pygame
from menu import Menu
from gameOver import GameOver
from game import Game
from howToPlay import HowToPlay
from settings import *
from options import *
import ctypes

if os.name == "nt":
    myappid = 'ayazearley.tonnetz.game.' + VERSION
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

pygame.init()
pygame.mixer.set_num_channels(60)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"Tonnetz v{VERSION}")
clock = pygame.time.Clock()

current_state = Menu(screen)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.mixer.music.load(os.path.join(BASE_DIR, "assets", "music", "AmbientNormalized.mp3"))
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(loops=-1)

icon_path = os.path.join(BASE_DIR, "assets", "images", "logo.png")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

running = True 
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_state.handle_event(event)

    current_state.update(dt)
    current_state.draw()

    if current_state.next_state == "game":
        current_state = Game(screen)
    elif current_state.next_state == "options":
            current_state = Options(screen)
    elif current_state.next_state == "gameover":
        current_state = GameOver(screen, current_state.winner, current_state.p1_score, current_state.p2_score)
    elif current_state.next_state == "menu":
        current_state = Menu(screen)
    elif current_state.next_state == "howToPlay":
        current_state = HowToPlay(screen)
    elif getattr(current_state, "next_state", None) is not None:
        current_state.next_state = None

    pygame.display.flip()

pygame.quit() 