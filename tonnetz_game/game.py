import pygame
import math
import settings
from node import *
import os
import random


CENTERX = SCREEN_WIDTH / 2
CENTERY = SCREEN_HEIGHT / 2

NODE_SPACING = 80
ROW_HEIGHT = NODE_SPACING * (math.sqrt(3) / 2)

Fs1.capture(PLAYER_2, playPing=False)
Gb2.capture(PLAYER_1, playPing=False)

Fs2.capture(PLAYER_2, playPing=False)
Gb1.capture(PLAYER_1, playPing=False)

TURN = PLAYER_1
P1done = False
P2done = False

def lerp_color(color_a, color_b, t):
    return tuple(a + (b - a) * t for a, b in zip(color_a, color_b))


def darken(color, factor=0.4):
    """factor: 0 = black, 1 = original color"""
    return tuple(int(c * factor) for c in color)

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


class Game:
    def __init__(self, screen):
        global TURN, P1done, P2done
        reset_game()
        TURN = PLAYER_1
        P1done = False
        P2done = False


        if settings.STARTING_POSITIONS == "balanced":
            Fs1.capture(PLAYER_2, playPing=False)
            Gb2.capture(PLAYER_1, playPing=False)
            Fs2.capture(PLAYER_2, playPing=False)
            Gb1.capture(PLAYER_1, playPing=False)

        elif settings.STARTING_POSITIONS == "split":
            Fs1.capture(PLAYER_2, playPing=False)
            Gb2.capture(PLAYER_2, playPing=False)
            Fs2.capture(PLAYER_1, playPing=False)
            Gb1.capture(PLAYER_1, playPing=False)

        elif settings.STARTING_POSITIONS == "random":
            sample = random.sample(ALL_NODES, 4)
            for node in sample[2:]:
                node.capture(PLAYER_1, playPing=False)
            for node in sample[:2]:
                node.capture(PLAYER_2, playPing=False)

        self.screen = screen
        self.next_state = None
        self.nodeFont = pygame.font.SysFont("corbel", 24)
        self.nodes = ALL_NODES
        self.turnFont = pygame.font.SysFont("corbel", 32)


        
    def handle_event(self, event):
        global TURN

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        available = get_available_nodes(TURN)
        
        for node in self.nodes:
            if node not in available:
                continue

            x, y = node.pos
            label_x, label_y = x, y - 20  # match draw()'s offset

            distance = ((event.pos[0] - label_x) ** 2 + (event.pos[1] - label_y) ** 2) ** 0.5

            if distance <= 25:
                node.capture(TURN)
                TURN = PLAYER_2 if TURN == PLAYER_1 else PLAYER_1
                return

    def update(self, dt):
        global TURN, P1done, P2done

        for node in self.nodes:
            if node.pulseTime > 0:
                node.pulseTime -= dt
            if node.pulseTime < 0:
                node.pulseTime = 0

        available = get_available_nodes(TURN)
        if len(available) == 0:
            if TURN == PLAYER_1:
                P1done = True
            else:
                P2done = True

            if P1done and P2done:
                p1_score = len(P1_TRIADS)
                p2_score = len(P2_TRIADS)

                if p1_score > p2_score:
                    self.winner = 1
                elif p2_score >= p1_score:
                    self.winner = 2

                self.p1_score = p1_score
                self.p2_score = p2_score
                self.next_state = "gameover"
                return 

            TURN = PLAYER_2 if TURN == PLAYER_1 else PLAYER_1


    def draw(self):
        self.screen.fill((21, 21, 21))

        if TURN == PLAYER_1:
            available = get_available_nodes(PLAYER_1)
            highlight_color = darken(P1COLOR)
        else:
            available = get_available_nodes(PLAYER_2)
            highlight_color = darken(P2COLOR)

        # Draw connection lines first, so labels render on top
        LINE_MARGIN = 22
        for node in self.nodes:
            if node.owner == 0:
                continue
            node_pos = (node.pos[0], node.pos[1] - 20)
            for neighbor in ADJACENCY.get(node, []):
                if neighbor.owner == node.owner:
                    neighbor_pos = (neighbor.pos[0], neighbor.pos[1] - 20)
                    start, end = shrink_line(node_pos, neighbor_pos, LINE_MARGIN)
                    
                    
                    if neighbor.pulseTime > 0 and node.pulseTime > 0:
                        t = node.pulseTime / PULSE_TIME
                        lineColor = lerp_color(node.color, COLOR3, t)
                    else:
                        lineColor = node.color
                    pygame.draw.line(self.screen, lineColor, start, end, 2)

        # Then draw the node labels on top of the lines
        for node in self.nodes:
            x, y = node.pos
            
            if node.pulseTime > 0:
                t = node.pulseTime / PULSE_TIME  # 1.0 = just triggered, 0.0 = faded out
                color = lerp_color(node.color, COLOR3, t)
            elif node.owner != 0:
                color = node.color
            elif node in available:
                color = highlight_color
            else:
                color = node.color

            label = self.nodeFont.render(node.name, True, color)
            label_rect = label.get_rect(center=(x, y - 20))
            self.screen.blit(label, label_rect)

        if TURN == PLAYER_1:
            turn_text = "Player 1's Turn"
            turn_color = P1COLOR
        else:
            turn_text = "Player 2's Turn"
            turn_color = P2COLOR

        turn_surface = self.turnFont.render(turn_text, True, turn_color)
        turn_rect = turn_surface.get_rect(center=(200, 50))
        self.screen.blit(turn_surface, turn_rect)


        p1_score = len(P1_TRIADS)
        p1_score_surface = self.turnFont.render("Player 1: " + str(p1_score), True, P1COLOR)
        p1_score_rect = turn_surface.get_rect(center=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50))
        self.screen.blit(p1_score_surface, p1_score_rect)

        p2_score = len(P2_TRIADS)
        p2_score_surface = self.turnFont.render("Player 2: " + str(p2_score), True, P2COLOR)
        p2_score_rect = turn_surface.get_rect(center=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 80))
        self.screen.blit(p2_score_surface, p2_score_rect)

        