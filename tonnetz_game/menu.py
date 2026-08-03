import math
import pygame
from settings import *
import decoNodes
from decoNodes import harpMenuPulses, crotalesMenuPulses, celesteMenuPulses
from background import create_tilted_gradient

FADE_SPEED = 3
PULSE_TIME = 3.5
PULSE_SYNC_OFFSET = 0.2

def get_global_time():
    return pygame.time.get_ticks() / 1000.0

def lerp_color(color_a, color_b, t): 
    return tuple(a + (b - a) * t for a, b in zip(color_a, color_b))

class Pulse:
    ATTACK_FRACTION = 0.2
    HOLD_FRACTION = 0.3

    def __init__(self, node, start_time, target_color, duration=PULSE_TIME):
        self.node = node
        self.start_time = start_time
        self.target_color = target_color
        self.duration = duration
        self.progress = 0.0
        self.active = False
        self.finished = False

    def update(self, elapsed_time):
        if elapsed_time < self.start_time:
            return
        self.active = True
        self.progress = (elapsed_time - self.start_time) / self.duration
        if self.progress >= 1.0:
            self.finished = True

    def get_color(self):
        if not self.active or self.finished:
            return None

        t = self.progress
        attack = self.ATTACK_FRACTION
        hold_end = attack + self.HOLD_FRACTION

        if t < attack:
            # sharp rise: full intensity almost immediately
            intensity = t / attack
        elif t < hold_end:
            # hold at full intensity
            intensity = 1.0
        else:
            # smooth ease back down to 0 over the remaining time
            decay_t = (t - hold_end) / (1.0 - hold_end)
            intensity = math.cos(decay_t * math.pi / 2)  # 1 -> 0

        color = lerp_color(self.node.color, self.target_color, intensity)
        return tuple(int(c) for c in color)

def shrink_line(pos_a, pos_b, margin):
    """Returns two points pulled inward from pos_a/pos_b by `margin` pixels each,
    so a line drawn between them leaves a gap for labels at both ends."""
    ax, ay = pos_a
    bx, by = pos_b

    dx = bx - ax
    dy = by - ay
    length = (dx ** 2 + dy ** 2) ** 0.5

    if length == 0:
        return pos_a, pos_b

    # unit vector pointing from a to b
    ux = dx / length
    uy = dy / length

    new_a = (ax + ux * margin, ay + uy * margin)
    new_b = (bx - ux * margin, by - uy * margin)

    return new_a, new_b

class Button:
    def __init__(self, text, font, center, normal_color, hover_color):
        self.text = text
        self.font = font
        self.center = center
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.hover_progress = 0.0

        temp = font.render(text, True, normal_color)
        self.rect = temp.get_rect(center=center)

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


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.next_state = None

        width = screen.get_width()

        self.titleFont = pygame.font.SysFont("corbel", 144)
        self.buttonFont = pygame.font.SysFont("corbel", 60)
        self.nodes = decoNodes.DECONODES1
        self.nodes2 = decoNodes.DECONODES2
        self.nodeFont = pygame.font.SysFont("corbel", 24)

        NORMAL = (255, 255, 255)


        self.background = create_tilted_gradient(
            screen.get_width(), screen.get_height(),
            (18, 18, 24), (32, 2, 48),
            angle=60
        )

        self.buttons = [
            Button("Start Game", self.buttonFont, (width // 2, 240), NORMAL, (0, 255, 255)),
            Button("Options", self.buttonFont, (width // 2, 320), NORMAL, (255, 0, 255)),
            Button("How to Play", self.buttonFont, (width // 2, 400), NORMAL, (255, 255, 0)),
            Button("Quit", self.buttonFont, (width // 2, 480), NORMAL, (100, 100, 100)),
        ]
        self.pulse_definitions = (
            list(harpMenuPulses) + list(crotalesMenuPulses) + list(celesteMenuPulses)
        )


        self.loop_length = 387.2

        self.elapsed_time = 0.0
        self.last_cycle_time = None
        self.pulses = []
        self._spawn_pulses()

    def _spawn_pulses(self):
        """(Re)builds the live Pulse objects from the raw definitions."""
        self.pulses = [
            Pulse(node, start_time, target_color)
            for node, start_time, _, target_color in self.pulse_definitions
        ]

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                self.handle_click(button.text)

    def handle_click(self, button_text):
        if button_text == "Start Game":
            self.next_state = "game"
        elif button_text == "Options":
            self.next_state = "options"
        elif button_text == "How to Play":
            self.next_state = "howToPlay"
        elif button_text == "Quit":
            pygame.quit()
            raise SystemExit

    def update(self, dt):
        # elapsed_time now tracks position within the loop, derived from the
        # global clock rather than accumulated dt, so it can't drift or reset
        cycle_time = (get_global_time() - PULSE_SYNC_OFFSET) % self.loop_length

        # if cycle_time just wrapped back to a smaller value than last frame,
        # a new loop started - respawn pulses so they fire again this cycle
        if self.last_cycle_time is not None and cycle_time < self.last_cycle_time:
            self._spawn_pulses()
        self.last_cycle_time = cycle_time
        self.elapsed_time = cycle_time

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(dt, mouse_pos)

        for pulse in self.pulses:
            pulse.update(self.elapsed_time)
        self.pulses = [p for p in self.pulses if not p.finished]

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        titleSurface = self.titleFont.render("Tonnetz", True, (255, 255, 255))
        titleRect = titleSurface.get_rect(center=(self.screen.get_width() // 2, 130))
        self.screen.blit(titleSurface, titleRect)

        for button in self.buttons:
            button.draw(self.screen)

        # collect current pulse colors, keyed by node identity, so the
        # line- and label-drawing loops below can use them in place of
        # each node's normal base color
        pulse_colors = {}
        for pulse in self.pulses:
            color = pulse.get_color()
            if color is not None:
                pulse_colors[id(pulse.node)] = color

        LINE_MARGIN = 22
        drawn_edges = set()
        for node in self.nodes:
            node_pos = (node.pos[0], node.pos[1] - 20)
            node_color = pulse_colors.get(id(node), node.color)
            for neighbor in decoNodes.ADJACENCY3.get(node, []):
                edge_key = frozenset((id(node), id(neighbor)))
                if edge_key in drawn_edges:
                    continue
                drawn_edges.add(edge_key)

                neighbor_pos = (neighbor.pos[0], neighbor.pos[1] - 20)
                neighbor_color = pulse_colors.get(id(neighbor), neighbor.color)
                start, end = shrink_line(node_pos, neighbor_pos, LINE_MARGIN)

                line_color = lerp_color(node_color, neighbor_color, 0.5)
                line_color = tuple(int(c) for c in line_color)
                pygame.draw.line(self.screen, line_color, start, end, 2)

        for node in self.nodes2:
            node_pos = (node.pos[0], node.pos[1] - 20)
            node_color = pulse_colors.get(id(node), node.color)
            for neighbor in decoNodes.ADJACENCY4.get(node, []):
                edge_key = frozenset((id(node), id(neighbor)))
                if edge_key in drawn_edges:
                    continue
                drawn_edges.add(edge_key)

                neighbor_pos = (neighbor.pos[0], neighbor.pos[1] - 20)
                neighbor_color = pulse_colors.get(id(neighbor), neighbor.color)
                start, end = shrink_line(node_pos, neighbor_pos, LINE_MARGIN)

                line_color = lerp_color(node_color, neighbor_color, 0.5)
                line_color = tuple(int(c) for c in line_color)
                pygame.draw.line(self.screen, line_color, start, end, 2)

        for node in self.nodes:
            x, y = node.pos
            color = pulse_colors.get(id(node), (100, 100, 100))
            label = self.nodeFont.render(node.name, True, color)
            label_rect = label.get_rect(center=(x, y - 20))
            self.screen.blit(label, label_rect)

        for node in self.nodes2:
            x, y = node.pos
            color = pulse_colors.get(id(node), (100, 100, 100))
            label = self.nodeFont.render(node.name, True, color)
            label_rect = label.get_rect(center=(x, y - 20))
            self.screen.blit(label, label_rect)