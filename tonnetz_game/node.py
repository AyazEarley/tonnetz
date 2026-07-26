from settings import *
import settings
import math 
import pygame
import os

pygame.init() 

CENTERX = SCREEN_WIDTH / 2
CENTERY = SCREEN_HEIGHT / 2

NODE_SPACING = 80
ROW_HEIGHT = NODE_SPACING * (math.sqrt(3) / 2)

P1_NODES = []
P2_NODES = []

P1_TRIADS = []
P2_TRIADS = []

PULSE_TIME = 2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOUND_NAMES = ["celeste", "crotales"]

SOUND_SETS = {}
for sound_name in SOUND_NAMES:
    sound_pings = [
        pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", sound_name, f"{i}.wav"))
        for i in range(12)
    ]
    SOUND_SETS[sound_name] = {
        "C":   sound_pings[0],
        "C#":  sound_pings[1],
        "Db":  sound_pings[1],
        "D":   sound_pings[2],
        "Ebb": sound_pings[2],
        "D#":  sound_pings[3],
        "Eb":  sound_pings[3],
        "E":   sound_pings[4],
        "Fb":  sound_pings[4],
        "F":   sound_pings[5],
        "E#":  sound_pings[5],
        "F#":  sound_pings[6],
        "Gb":  sound_pings[6],
        "G":   sound_pings[7],
        "G#":  sound_pings[8],
        "Ab":  sound_pings[8],
        "A":   sound_pings[9],
        "Bbb": sound_pings[9],
        "A#":  sound_pings[10],
        "Bb":  sound_pings[10],
        "B":   sound_pings[11],
        "Cb":  sound_pings[11],
    }


for sound_dict in SOUND_SETS.values():
    for ping in sound_dict.values():
        ping.set_volume(PING_VOLUME)

def reset_game():
    global P1_NODES, P2_NODES, P1_TRIADS, P2_TRIADS

    for node in ALL_NODES:
        node.owner = 0
        node.color = (255, 255, 255)
        node.pulseTime = 0.0

    P1_NODES.clear()
    P2_NODES.clear()
    P1_TRIADS.clear()
    P2_TRIADS.clear()

class Node:
    def __init__(self, name, x, y, owner=0):
        self.name = name
        self.pos = (x, y)
        self.owner = 0
        self.color = (255, 255, 255)
        self.pulseTime = 0.0

        

    def capture(self, player, playPing = True):
        self.owner = player
        if(player == PLAYER_1):
            self.color=P1COLOR
            P1_NODES.append(self)
        else:
            self.color = P2COLOR
            P2_NODES.append(self)
        
        pingMe = set()
        pingMe.add(self.name)

        #check for triad
        same_owner_neighbors = [n for n in ADJACENCY.get(self, []) if n.owner == player]

        for i in range(len(same_owner_neighbors)):
            for j in range(i + 1, len(same_owner_neighbors)):
                node_a = same_owner_neighbors[i]
                node_b = same_owner_neighbors[j]

                if node_b in ADJACENCY.get(node_a, []):
                    triad = frozenset([self, node_a, node_b])
                    pingMe.add(node_a.name)
                    pingMe.add(node_b.name)
                    triad_list = P1_TRIADS if player == PLAYER_1 else P2_TRIADS

                    if triad not in triad_list:
                        triad_list.append(triad)
                    for n in (self, node_a, node_b):
                            n.pulseTime = PULSE_TIME 
        
        for name in pingMe:
            if playPing:
                current_getPing = SOUND_SETS.get(settings.P1SOUND, SOUND_SETS["celeste"])
                current_getPing[name].play()

        
 
#row 1
Ebb2 = Node("Ebb", CENTERX + (NODE_SPACING * .5), CENTERY - (ROW_HEIGHT * 3))
Bbb2 = Node("Bbb", CENTERX + (NODE_SPACING * 1.5), CENTERY - (ROW_HEIGHT * 3))

#row 2
Ebb1 = Node("Ebb", CENTERX - (NODE_SPACING * 3), CENTERY - (ROW_HEIGHT * 2))
Bbb1 = Node("Bbb", CENTERX - (NODE_SPACING * 2), CENTERY - (ROW_HEIGHT * 2))
Fb = Node("Fb", CENTERX - (NODE_SPACING * 1), CENTERY - (ROW_HEIGHT * 2))
Cb2 = Node("Cb", CENTERX, CENTERY - (ROW_HEIGHT * 2))
Gb2 = Node("Gb", CENTERX + (NODE_SPACING * 1), CENTERY - (ROW_HEIGHT * 2))
Db2 = Node("Db", CENTERX + (NODE_SPACING * 2), CENTERY - (ROW_HEIGHT * 2))

# row 3
Cb1 = Node("Cb", CENTERX - (NODE_SPACING * 3) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT)
Gb1 = Node("Gb", CENTERX - (NODE_SPACING * 2) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT)
Db1 = Node("Db", CENTERX - (NODE_SPACING * 1) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT)
Ab = Node("Ab", CENTERX - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT)
Eb2 = Node("Eb", CENTERX + (NODE_SPACING * 1) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT)
Bb2 = Node("Bb", CENTERX + (NODE_SPACING * 2) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT)
F2 = Node("F", CENTERX + (NODE_SPACING * 3) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT)

# row 4
A2 = Node("A", CENTERX + (NODE_SPACING * 3), CENTERY)
D2 = Node("D", CENTERX + (NODE_SPACING * 2), CENTERY)
G2 = Node("G", CENTERX + NODE_SPACING, CENTERY)
C = Node("C", CENTERX, CENTERY)
F1 = Node("F", CENTERX - NODE_SPACING, CENTERY)
Bb1 = Node("Bb", CENTERX - (NODE_SPACING * 2), CENTERY)
Eb1 = Node("Eb", CENTERX - (NODE_SPACING * 3), CENTERY)

# row 5
G1 = Node("G", CENTERX + (NODE_SPACING / 2) - (NODE_SPACING * 3), CENTERY + ROW_HEIGHT)
D1 = Node("D", CENTERX + (NODE_SPACING / 2) - (NODE_SPACING * 2), CENTERY + ROW_HEIGHT)
A1 = Node("A", CENTERX + (NODE_SPACING / 2) - (NODE_SPACING * 1), CENTERY + ROW_HEIGHT)
E = Node("E", CENTERX + (NODE_SPACING / 2), CENTERY + ROW_HEIGHT)
B2 = Node("B", CENTERX + (NODE_SPACING / 2) + (NODE_SPACING * 1), CENTERY + ROW_HEIGHT)
Fs2 = Node("F#", CENTERX + (NODE_SPACING / 2) + (NODE_SPACING * 2), CENTERY + ROW_HEIGHT)
Cs2 = Node("C#", CENTERX + (NODE_SPACING / 2) + (NODE_SPACING * 3), CENTERY + ROW_HEIGHT)


# row 6
B1 = Node("B", CENTERX - (NODE_SPACING * 2), CENTERY + (ROW_HEIGHT * 2))
Fs1 = Node("F#", CENTERX - (NODE_SPACING), CENTERY + (ROW_HEIGHT * 2))
Cs1 = Node("C#", CENTERX, CENTERY + (ROW_HEIGHT * 2))
Gs = Node("G#", CENTERX + (NODE_SPACING), CENTERY + (ROW_HEIGHT * 2))
Ds2 = Node("D#", CENTERX + (NODE_SPACING * 2), CENTERY + (ROW_HEIGHT * 2))
As2 = Node("A#", CENTERX + (NODE_SPACING * 3), CENTERY + (ROW_HEIGHT * 2))

#row 7
Ds1 = Node("D#", CENTERX - (NODE_SPACING * 1.5), CENTERY + (ROW_HEIGHT * 3))
As1 = Node("A#", CENTERX - (NODE_SPACING * 0.5), CENTERY + (ROW_HEIGHT * 3))

ALL_NODES = [C, F1, Bb1, Eb1, A2, D2, G2, 
             Ab, Db1, Gb1, Cb1, Eb2, Bb2, F2, Ebb1, Bbb1, 
             Fb, Cb2, Gb2, Db2, Ebb2, Bbb2, 
             E, A1, D1, G1, B2, Fs2, Cs2,
             Gs, Cs1, Fs1, B1, Ds2, As2,
             Ds1, As1
             ]

ADJACENCY = {
    #row 1
    Ebb2 : [Bbb2, Cb2, Gb2],
    Bbb2 : [Ebb2, Gb2, Db2],

    #row 2
    Ebb1 : [Bbb1, Cb1, Gb1],
    Bbb1 : [Ebb1, Gb1, Db1, Fb],
    Fb : [Bbb1, Db1, Ab, Cb2],
    Cb2: [Fb, Ab, Eb2, Gb2, Ebb2],
    Gb2 : [Cb2, Eb2, Bb2, Db2, Bbb2, Ebb2],
    Db2 : [Gb2, Bb2, F2, Bbb2],

    #row 3
    Cb1 : [Ebb1, Gb1, Eb1],
    Gb1 : [Cb1, Ebb1, Bbb1, Db1, Bb1, Eb1],
    Db1 : [Gb1, Bbb1, Fb, Ab, Bb1, F1],
    Ab : [Db1, Fb, Cb2, Eb2, C, F1], 
    Eb2 : [Ab, Cb2, Gb2, Bb2, G2, C],
    Bb2 : [Eb2, G2, D2, F2, Gb2, Db2],
    F2 : [Db2, Bb2, D2, A2],

    #row 4
    Eb1 : [Cb1, Gb1, Bb1, G1],
    Bb1 : [Eb1, G1, D1, F1, Db1, Gb1],
    F1 : [Bb1, D1, A1, C, Ab, Db1],
    C : [F1, A1, E, G2, Eb2, Ab],
    G2 : [C, E, B2, D2, Bb2, Eb2],
    D2: [G2, B2, Fs2, A2, F2, Bb2],
    A2: [D2, Fs2, F2, Cs2],

    #row 5
    G1 : [Eb1, Bb1, D1, B1],
    D1 : [G1, Bb1, F1, A1, B1, Fs1],
    A1 : [D1, F1, C, E, Cs1, Fs1],
    E : [A1, Cs1, Gs, C, G2, B2],
    B2 : [G2, E, Gs, Ds2, Fs2, D2],
    Fs2 : [B2, Ds2, As2, Cs2, A2, D2],
    Cs2 : [Fs2, As2, A2],

    #row 6
    B1 : [G1, D1, Fs1, Ds1],
    Fs1 : [B1, Ds1, As1, Cs1, A1, D1],
    Cs1 : [Fs1, As1, Gs, E, A1],
    Gs : [Cs1, Ds2, B2, E],
    Ds2 : [Gs, As2, Fs2, B2],
    As2 : [Ds2, Fs2, Cs2],

    #row 7
    Ds1 : [B1, Fs1, As1],
    As1 : [Ds1, Fs1, Cs1]
}

def get_available_nodes(player):
    """
    Returns a list of unowned nodes adjacent to any node the given
    player already owns, plus any unowned nodes sharing a name with
    one they own - i.e. their valid "expansion" options.
    """
    owned = P1_NODES if player == PLAYER_1 else P2_NODES
    owned_names = {node.name for node in owned}

    available = set()
    for node in owned:
        for neighbor in ADJACENCY.get(node, []):
            if neighbor.owner == 0:  # not yet captured by anyone
                available.add(neighbor)

    for node in ALL_NODES:
        if node.owner == 0 and node.name in owned_names:
            available.add(node)

    return list(available)