from node import Node
import math
from settings import *
import midi
import random

from game import NODE_SPACING, ROW_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH

CENTERX = SCREEN_WIDTH / 2
CENTERY = SCREEN_HEIGHT / 2

BOTTOMX = SCREEN_HEIGHT + 40

Abb3 = Node("Abb", 600 + NODE_SPACING, BOTTOMX - (ROW_HEIGHT * 6), owner=3)

Fb3 = Node("Fb", 600 + (NODE_SPACING / 2), BOTTOMX - (ROW_HEIGHT * 5), owner=3)
Cb3 = Node("Cb", 600 + (NODE_SPACING / 2) + NODE_SPACING, BOTTOMX - (ROW_HEIGHT * 5), owner=3)

Db3 = Node("Db", 600, BOTTOMX - (ROW_HEIGHT * 4), owner=3)
Ab3 = Node("Ab", 600 + NODE_SPACING, BOTTOMX - (ROW_HEIGHT * 4), owner=3)

F3 = Node("F", 600 + (NODE_SPACING / 2), BOTTOMX - (ROW_HEIGHT * 3), owner=3)
C3 = Node("C", 600 + (NODE_SPACING / 2) + NODE_SPACING, BOTTOMX - (ROW_HEIGHT * 3), owner=3)

E3 = Node("E", 600 + (NODE_SPACING * 2), BOTTOMX - (ROW_HEIGHT * 2), owner=3)
D3 = Node("D", 600, BOTTOMX - (ROW_HEIGHT * 2), owner=3)
A3 = Node("A", 600 + NODE_SPACING, BOTTOMX - (ROW_HEIGHT * 2), owner=3)

Fs3 = Node("F#", 600 + (NODE_SPACING / 2), BOTTOMX - ROW_HEIGHT, owner=3)
Cs3 = Node("C#", 600 + (NODE_SPACING / 2) + NODE_SPACING, BOTTOMX - ROW_HEIGHT, owner=3)

Ds3 = Node("D#", 600, BOTTOMX, owner=3)
As3 = Node("D#", 600 + NODE_SPACING, BOTTOMX, owner=3)

DECONODES1 = [Ds3, Fs3, As3, Cs3, D3, A3,E3, F3, C3, Db3, Ab3, Fb3, Abb3, Cb3]

ADJACENCY3 = {
    #row 1
    Ds3 : [Fs3, As3],
    As3 : [Ds3, Fs3, Cs3],

    Fs3 : [Ds3, As3, Cs3, D3, A3],
    Cs3 : [As3, Fs3, A3, E3],

    D3 : [Fs3, F3, A3],
    A3 : [D3, Fs3, F3, C3, E3, Cs3],
    E3 : [A3, Cs3, C3],

    F3 : [D3, Db3, Ab3, C3, A3],
    C3 : [A3, E3, F3, Ab3],

    Db3 : [F3, Ab3, Fb3],
    Ab3 : [F3, C3, Fb3, Cb3],

    Fb3 : [Db3, Ab3, Abb3, Cb3],
    Abb3: [Fb3, Cb3],

    Cb3: [Abb3, Ab3, Cb3]

    
}

startX = 10
TOPY = -10

Ebb4 = Node("Ebb", startX, TOPY, owner=3)
Bbb4 = Node("Bbb", startX + NODE_SPACING, TOPY, owner=3)

Gb4 = Node("Gb", startX + (NODE_SPACING / 2), TOPY + ROW_HEIGHT, owner=3)
Db4 = Node("Db", startX + (NODE_SPACING / 2) + NODE_SPACING, TOPY + ROW_HEIGHT, owner=3)

Bb4 = Node("Bb", startX + NODE_SPACING, TOPY + (ROW_HEIGHT * 2), owner=3)

G4 = Node("G", startX + (NODE_SPACING / 2), TOPY + (ROW_HEIGHT * 3), owner=3)
D4 = Node("D", startX + (NODE_SPACING / 2) + NODE_SPACING, TOPY + (ROW_HEIGHT * 3), owner=3)

B4 = Node("B", startX + NODE_SPACING, TOPY + (ROW_HEIGHT * 4), owner=3)
Fs4 = Node("F#", startX + (NODE_SPACING * 2), TOPY + (ROW_HEIGHT * 4), owner=3)

Ds4 = Node("D#", startX + (NODE_SPACING / 2) + NODE_SPACING, TOPY + (ROW_HEIGHT * 5), owner=3)
As4 = Node("A#", startX + (NODE_SPACING / 2) + (NODE_SPACING * 2), TOPY + (ROW_HEIGHT * 5), owner=3)

Bs4 = Node("B#", startX + NODE_SPACING, TOPY + (ROW_HEIGHT * 6), owner=3)
Fss4 = Node("Fx", startX + (NODE_SPACING * 2), TOPY + (ROW_HEIGHT * 6), owner=3)

Dss4 = Node("Dx", startX + (NODE_SPACING / 2) + NODE_SPACING, TOPY + (ROW_HEIGHT * 7), owner=3)

DECONODES2 = [Ebb4, Bbb4, Gb4, Db4, Bb4, G4, D4, B4, Fs4, Ds4, As4, Bs4, Fss4, Dss4]


ADJACENCY4 = {
    Ebb4 : [Bbb4, Gb4],
    Bbb4 : [Ebb4, Gb4, Db4],

    Gb4 : [Ebb4, Db4, Bb4],
    Db4 : [Gb4, Bbb4, Bb4],

    Bb4 : [Gb4, Db4, G4, D4],

    G4 : [Bb4, D4, B4],
    D4 : [B4, G4, Bb4, Fs4],

    B4 : [G4, D4, Fs4, Ds4],
    Fs4 : [B4, D4, Ds4, As4],

    Ds4 : [B4, Fs4, As4],
    As4 : [Fs4, Ds4, Fss4],

    Bs4 : [Ds4, Fss4, Dss4],
    Fss4 : [Dss4, Bs4, Ds4],

    Dss4 : [Bs4, Fss4]

}

celestePing = [A3,C3,F3, E3, Cs3]
harpPing = [Fs4, Ds4, As4, Fss4]
crotalesPing = [D4, Bs4, Abb3, D3]

random.shuffle(celestePing)
random.shuffle(harpPing)
random.shuffle(crotalesPing)

celesteMenuPulses = []
count = 0
for event in midi.celesteEvents:
    celesteMenuPulses.append([celestePing[count % len(celestePing)],event.start, event.end - event.start, COLOR3])
    count += 1

crotalesMenuPulses = []
for event in midi.crotalesEvents:
    crotalesMenuPulses.append([crotalesPing[count % len(crotalesPing)],event.start, event.end - event.start, P1COLOR])
    count += 1

harpMenuPulses = []
for event in midi.harpEvents:
    harpMenuPulses.append([harpPing[count % len(harpPing)],event.start, event.end - event.start, P2COLOR])
    count += 1

for node in DECONODES1 + DECONODES2:
    node.color = (100,100,100)