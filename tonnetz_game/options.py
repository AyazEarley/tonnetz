import pygame
import settings
from node import SOUND_SETS

def lerp_color(color_a, color_b, t):
    return tuple(a + (b - a) * t for a, b in zip(color_a, color_b))
FADE_SPEED = 8  # progress units per second

class Slider:
    def __init__(self, pos, length, color, minVal, maxVal, startingValue, text):
        self.position = pos
        self.length = length
        self.height = 5
        self.color = color

        self.minVal = minVal
        self.maxVal = maxVal
        self.startingValue = startingValue

        self.text = text
        
        self.dragging = False

        circleX = self.position[0] - (self.length // 2) + (self.length * startingValue)

        self.circlePos = [circleX ,  self.position[1]]

        self.scoreFont = pygame.font.SysFont("corbel", 24)

    def draw(self, screen):
        pygame.draw.rect(
            screen, (180, 180, 180),
            (self.position[0] - (self.length // 2), self.position[1] - (self.height // 2), self.length, self.height),
            border_radius=3
        )
        pygame.draw.circle(
            screen, (180, 180, 180),
            (self.circlePos[0], self.circlePos[1]),
            radius=10
        )

        # Label on the left of the track
        labelSurface = self.scoreFont.render(self.text, True, (255, 255, 255))
        labelRect = labelSurface.get_rect(
            midright=(self.position[0] - (self.length // 2) - 15, self.position[1])
        )
        screen.blit(labelSurface, labelRect)

        # Live percentage on the right of the track
        percent = int(self.getValue() * 100)
        percentSurface = self.scoreFont.render(f"{percent}%", True, (255, 255, 255))
        percentRect = percentSurface.get_rect(
            midleft=(self.position[0] + (self.length // 2) + 15, self.position[1])
        )
        screen.blit(percentSurface, percentRect)

    def handle_click(self, mousePos):
        circle_x, circle_y = self.circlePos
        dx = mousePos[0] - circle_x
        dy = mousePos[1] - circle_y
        if (dx * dx + dy * dy) ** 0.5 <= 10:
            self.dragging = True

    def handle_drag(self, mousePos):

        if not self.dragging:
            return

        left = self.position[0] - (self.length // 2)
        right = self.position[0] + (self.length // 2)

        x = mousePos[0]
        x = max(left, min(x, right))

        self.circlePos[0] = x

    def handle_unclick(self):
        self.dragging = False

    def getValue(self):
        left = self.position[0] - (self.length // 2)
        distance = self.circlePos[0] - left

        proportion = distance / self.length

        valRange = self.maxVal - self.minVal
        return (valRange * proportion) + self.minVal


class Button:
    def __init__(self, text, font, center, normal_color, hover_color, action=None):
        self.text = text
        self.font = font
        self.center = center
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.hover_progress = 0.0
        self.action = action if action is not None else text  # defaults to text if not given

        temp = font.render(text, True, normal_color)
        self.rect = temp.get_rect(center=center)

    def set_text(self, new_text):
        """Update the button's label and recompute its rect, keeping the same center."""
        self.text = new_text
        temp = self.font.render(new_text, True, self.normal_color)
        self.rect = temp.get_rect(center=self.center)

    def update(self, dt, mouse_pos):
        is_hovering = self.rect.collidepoint(mouse_pos)
        target = 1.0 if is_hovering else 0.0

        if self.hover_progress < target:
            self.hover_progress = min(target, self.hover_progress + FADE_SPEED * dt)
        else:
            self.hover_progress = max(target, self.hover_progress - FADE_SPEED * dt)

    def draw(self, screen):
        color = lerp_color(self.normal_color, self.hover_color, self.hover_progress)
        color = tuple(int(c) for c in color)
        surface = self.font.render(self.text, True, color)
        screen.blit(surface, self.rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
    
    def set_hover_color(self, new_color):
        """Update the color the button fades to on hover."""
        self.hover_color = new_color

class Options:
    def __init__(self, screen):
        self.screen = screen
        self.next_state = None

        width = screen.get_width()

        self.titleFont = pygame.font.SysFont("corbel", 84)
        self.scoreFont = pygame.font.SysFont("corbel", 24)
        self.buttonFont = pygame.font.SysFont("corbel", 36) 

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
            Button(f"P1 Mode: {settings.P1MODE}", self.buttonFont, (width // 2, 140), NORMAL, settings.P1COLOR, "p1changeMode"),
            Button(f"P1 Color: {p1ColorText}", self.buttonFont, (width // 2, 180), NORMAL, settings.P1COLOR, "p1changeColor"),

            Button(f"P2 Mode: {settings.P2MODE}", self.buttonFont, (width // 2, 230), NORMAL, settings.P2COLOR, "p2changeMode"),
            Button(f"P2 Color: {p2ColorText}", self.buttonFont, (width // 2, 270), NORMAL, settings.P2COLOR, "p2changeColor"),

            Button(f"Starting Spots: {settings.STARTING_POSITIONS}", self.buttonFont, (width // 2, 320), NORMAL, settings.COLOR3, "changeStart"),
            Button(f"Ping Sound: {settings.P1SOUND}", self.buttonFont, (width // 2, 360), NORMAL, settings.COLOR3, "changePing"),

            

            Button("Back to Menu", self.buttonFont, (width // 2, 525), NORMAL, (100, 100, 100), "menu"),
            
        ]
        self.button_by_action = {b.action: b for b in self.buttons}

        length = 200
        self.slider = Slider((width // 2, 420), length, settings.COLOR3, 0, 1, settings.MUSIC_VOLUME, "Music:")
        self.slider2 = Slider((width // 2, 460), length, settings.COLOR3, 0, 1, settings.PING_VOLUME, "SFX:")

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                self.handle_click(button)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.slider.handle_click(event.pos)
            self.slider2.handle_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.slider.handle_drag(event.pos)
            self.slider2.handle_drag(event.pos)
            if self.slider.dragging:
                settings.MUSIC_VOLUME = self.slider.getValue()
                pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)

            if self.slider2.dragging:
                settings.PING_VOLUME = self.slider2.getValue()
                              
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.slider.handle_unclick()
            self.slider2.handle_unclick()
            settings.save_settings()
            for sound_dict in SOUND_SETS.values():
                for ping in sound_dict.values():
                    ping.set_volume(settings.PING_VOLUME)
            

    def handle_click(self, button):
        if button.action == "p1changeMode":
            settings.P1MODE = "player" if settings.P1MODE == "AI" else "AI"
            button.set_text(f"P1 Mode: {settings.P1MODE}")
            settings.save_settings()
        elif button.action == "p1changeColor":
            settings.P1COLOR, settings.COLOR3 = settings.COLOR3, settings.P1COLOR

            if settings.P1COLOR == (255, 0, 255):
                text = "magenta"
            elif settings.P1COLOR == (255, 255, 0):
                text = "yellow"
            else:
                text = "cyan"

            button.set_text(f"P1 Color: {text}")
            button.set_hover_color(settings.P1COLOR)
            self.button_by_action["p1changeMode"].set_hover_color(settings.P1COLOR)
            self.button_by_action["changeStart"].set_hover_color(settings.COLOR3)
            self.button_by_action["changePing"].set_hover_color(settings.COLOR3)
            settings.save_settings()

        elif button.action == "p2changeMode":
            settings.P2MODE = "player" if settings.P2MODE == "AI" else "AI"
            button.set_text(f"P2 Mode: {settings.P2MODE}")
            settings.save_settings()
        elif button.action == "p2changeColor":
            settings.P2COLOR, settings.COLOR3 = settings.COLOR3, settings.P2COLOR

            if settings.P2COLOR == (255, 0, 255):
                text = "magenta"
            elif settings.P2COLOR == (255, 255, 0):
                text = "yellow"
            else:
                text = "cyan"
            
            button.set_text(f"P2 Color: {text}")
            button.set_hover_color(settings.P2COLOR)
            self.button_by_action["p2changeMode"].set_hover_color(settings.P2COLOR)
            self.button_by_action["changeStart"].set_hover_color(settings.COLOR3)
            self.button_by_action["changePing"].set_hover_color(settings.COLOR3)
            settings.save_settings()

        elif button.action == "changeStart":
            carosel = ["balanced", "split", "random"]
            index = carosel.index(settings.STARTING_POSITIONS)

            settings.STARTING_POSITIONS = carosel[(index + 1) % len(carosel)]
            button.set_text(f"Starting Spots: {settings.STARTING_POSITIONS}")
            settings.save_settings()

        elif button.action == "changePing":
            carosel = ["celeste", "crotales"]
            index = carosel.index(settings.P1SOUND)
        
            settings.P1SOUND = carosel[(index + 1) % len(carosel)]
            button.set_text(f"Ping Sound: {settings.P1SOUND}")
            settings.save_settings()

        elif button.action == "menu":
            self.next_state ="menu"
            settings.save_settings()
            

        

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(dt, mouse_pos)

    def draw(self):
        self.screen.fill((21, 21, 21))

        titleSurface = self.titleFont.render("Options", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(self.screen.get_width() // 2, 70))
        self.screen.blit(titleSurface, titleRect)

        for button in self.buttons:
            button.draw(self.screen)

        self.slider.draw(self.screen)
        self.slider2.draw(self.screen)

        