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

Dbb5 = Node("Dbb", CENTERX - (NODE_SPACING * 5), CENTERY - (ROW_HEIGHT * 2), owner=3)

Bbb5 = Node("Bbb", CENTERX - (NODE_SPACING * 5) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT, owner=3)
Fb5 = Node("Fb", CENTERX - (NODE_SPACING * 4) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT, owner=3)

Db5 = Node("Db", CENTERX - (NODE_SPACING * 5), CENTERY, owner=3)
Ab5 = Node("Ab", CENTERX - (NODE_SPACING * 4), CENTERY, owner=3)

Bb5 = Node("Bb", CENTERX + (NODE_SPACING / 2) - (NODE_SPACING * 6), CENTERY + ROW_HEIGHT, owner=3)
F5 = Node("F", CENTERX + (NODE_SPACING / 2) - (NODE_SPACING * 5), CENTERY + ROW_HEIGHT, owner=3)
C5 = Node("C", CENTERX + (NODE_SPACING / 2) - (NODE_SPACING * 4), CENTERY + ROW_HEIGHT, owner=3)

D5 = Node("D", CENTERX - (NODE_SPACING * 5), CENTERY + (ROW_HEIGHT * 2), owner=3)
A5 = Node("A", CENTERX - (NODE_SPACING * 4), CENTERY + (ROW_HEIGHT * 2), owner=3)
E5 = Node("E", CENTERX - (NODE_SPACING * 3), CENTERY + (ROW_HEIGHT * 2), owner=3)

#
Gs5 = Node("G#", CENTERX - (NODE_SPACING * 2.5), CENTERY + (ROW_HEIGHT * 3), owner=3)
Cs5 = Node("C#", CENTERX - (NODE_SPACING * 3.5), CENTERY + (ROW_HEIGHT * 3), owner=3)
Fs5 = Node("F#", CENTERX - (NODE_SPACING * 4.5), CENTERY + (ROW_HEIGHT * 3), owner=3)
B5 = Node("B", CENTERX - (NODE_SPACING * 5.5), CENTERY + (ROW_HEIGHT * 3), owner=3)

Bs5 = Node("B#", CENTERX - (NODE_SPACING * 2), CENTERY + (ROW_HEIGHT * 4), owner=3)
Es5 = Node("E#", CENTERX - (NODE_SPACING * 3), CENTERY + (ROW_HEIGHT * 4), owner=3)
As5 = Node("A#", CENTERX - (NODE_SPACING * 4), CENTERY + (ROW_HEIGHT * 4), owner=3)
Ds5 = Node("D#", CENTERX - (NODE_SPACING * 5), CENTERY + (ROW_HEIGHT * 4), owner=3)

Dss5 = Node("Dx", CENTERX - (NODE_SPACING * 1.5), CENTERY + (ROW_HEIGHT * 5), owner=3)
Gss5 = Node("Gx", CENTERX - (NODE_SPACING * 2.5), CENTERY + (ROW_HEIGHT * 5), owner=3)
Css5 = Node("Cx", CENTERX - (NODE_SPACING * 3.5), CENTERY + (ROW_HEIGHT * 5), owner=3)
Fss5 = Node("Fx", CENTERX - (NODE_SPACING * 4.5), CENTERY + (ROW_HEIGHT * 5), owner=3)

Bs6 = Node("B#", CENTERX + (NODE_SPACING * 5), CENTERY + (ROW_HEIGHT * 2), owner=3)
Gs6 = Node("G#", CENTERX + (NODE_SPACING / 2) + (NODE_SPACING * 4), CENTERY + ROW_HEIGHT, owner=3)
Ds6 = Node("D#", CENTERX + (NODE_SPACING / 2) + (NODE_SPACING * 5), CENTERY + ROW_HEIGHT, owner=3)

E6 = Node("E", CENTERX + (NODE_SPACING * 4), CENTERY, owner=3)
B6 = Node("B", CENTERX + (NODE_SPACING * 5), CENTERY, owner=3)

C6 = Node("C", CENTERX + (NODE_SPACING * 4) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT, owner=3)
G6 = Node("G", CENTERX + (NODE_SPACING * 5) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT, owner=3)
D6 = Node("D", CENTERX + (NODE_SPACING * 6) - (NODE_SPACING / 2), CENTERY - ROW_HEIGHT, owner=3)

Ab6 = Node("Ab", CENTERX + (NODE_SPACING * 3), CENTERY - (ROW_HEIGHT * 2), owner=3)
Eb6 = Node("Eb", CENTERX + (NODE_SPACING * 4), CENTERY - (ROW_HEIGHT * 2), owner=3)
Bb6 = Node("Bb", CENTERX + (NODE_SPACING * 5), CENTERY - (ROW_HEIGHT * 2), owner=3)

Fb6 = Node("Fb", CENTERX + (NODE_SPACING * 2.5), CENTERY - (ROW_HEIGHT * 3), owner=3)
Cb6 = Node("Cb", CENTERX + (NODE_SPACING * 3.5), CENTERY - (ROW_HEIGHT * 3), owner=3)
Gb6 = Node("Gb", CENTERX + (NODE_SPACING * 4.5), CENTERY - (ROW_HEIGHT * 3), owner=3)
Db6 = Node("Fb", CENTERX + (NODE_SPACING * 5.5), CENTERY - (ROW_HEIGHT * 3), owner=3)

Dbb6 = Node("Dbb", CENTERX + (NODE_SPACING * 2), CENTERY - (ROW_HEIGHT * 4), owner=3)
Abb6 = Node("Abb", CENTERX + (NODE_SPACING * 3), CENTERY - (ROW_HEIGHT * 4), owner=3)
Ebb6 = Node("Ebb", CENTERX + (NODE_SPACING * 4), CENTERY - (ROW_HEIGHT * 4), owner=3)
Bbb6 = Node("Bbb", CENTERX + (NODE_SPACING * 5), CENTERY - (ROW_HEIGHT * 4), owner=3)

DECONODES3 = [
    Gs5, Cs5, Fs5, B5, E5, A5, D5, C5, F5, Bb5, Ab5, Db5, Bbb5, Fb5, Bs5, Es5, As5, Ds5, Dss5, Gss5, Css5, Fss5, Dbb5,
    Bs6, Gs6, Ds6, E6, B6, C6, G6, D6, Ab6, Eb6, Bb6, Fb6, Cb6, Gb6, Db6, Dbb6, Abb6, Ebb6, Bbb6
              ]

for node in DECONODES1 + DECONODES2:
    node.color = (100,100,100)

for node in DECONODES3:
    node.color = (50,50,50)

ADJACENCY5 = {
    Dss5 : [Bs5],
    Gss5 : [Es5, Bs5],
    Css5 : [As5, Es5],
    Fss5 : [As5, Ds5],

    Bs5 : [Gs5, Es5],
    Es5 : [Gs5, Bs5, Cs5, As5],
    As5 : [Cs5, Fs5, Ds5],

    Gs5 : [Cs5, E5,],
    Cs5: [E5, A5, Fs5],
    Fs5 : [Ds5, B5, D5, A5],

    E5 : [C5, A5,],
    A5 : [C5, F5],
    D5 : [F5, A5],

    C5: [F5, Ab5],
    F5 : [Bb5, Ab5, Db5],

    Ab5 : [Fb5, Db5],
    Fb5 : [Bbb5, Dbb5, Db5],

    Bs6 : [Gs6],
    Gs6 : [Ds6, E6, B6],
    E6 : [B6, C6, G6],
    B6 : [G6],
    C6 : [Ab6 , Eb6, G6],
    G6 : [Eb6, Bb6, D6],

    Ab6 : [Fb6, Cb6, Eb6],
    Eb6 : [Cb6, Gb6, Bb6],
    Bb6 : [Gb6],

    Fb6 : [Dbb6, Abb6, Cb6],
    Cb6 : [Abb6, Ebb6, Gb6],
    Gb6 : [Db6, Ebb6, Bbb6],

    Dbb6 : [Abb6,],
    Abb6 : [Ebb6],
    Ebb6 : [Bbb6]

    
}