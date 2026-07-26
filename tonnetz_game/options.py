import pygame
import settings

def lerp_color(color_a, color_b, t):
    return tuple(a + (b - a) * t for a, b in zip(color_a, color_b))
FADE_SPEED = 8  # progress units per second


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
        self.scoreFont = pygame.font.SysFont("corbel", 36)
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
            Button(f"P1 Mode: {settings.P1MODE}", self.buttonFont, (width // 2, 150), NORMAL, settings.P1COLOR, "p1changeMode"),
            Button(f"P1 Color: {p1ColorText}", self.buttonFont, (width // 2, 200), NORMAL, settings.P1COLOR, "p1changeColor"),

            Button(f"P2 Mode: {settings.P2MODE}", self.buttonFont, (width // 2, 275), NORMAL, settings.P2COLOR, "p2changeMode"),
            Button(f"P2 Color: {p2ColorText}", self.buttonFont, (width // 2, 325), NORMAL, settings.P2COLOR, "p2changeColor"),

            Button(f"Starting Spots: {settings.STARTING_POSITIONS}", self.buttonFont, (width // 2, 400), NORMAL, settings.COLOR3, "changeStart"),
            Button(f"Ping Sound: {settings.P1SOUND}", self.buttonFont, (width // 2, 450), NORMAL, settings.COLOR3, "changePing"),

            Button("Back to Menu", self.buttonFont, (width // 2, 525), NORMAL, (100, 100, 100), "menu"),
            
        ]
        self.button_by_action = {b.action: b for b in self.buttons}

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                self.handle_click(button)

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