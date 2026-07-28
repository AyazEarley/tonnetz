from node import *
import random

NAME_LOOKUP = {}
for n in ALL_NODES:
    NAME_LOOKUP.setdefault(n.name, []).append(n)

# Fixed order used to build a hashable snapshot of ownership for the transposition table.
ALL_NODES_ORDERED = list(ALL_NODES)

# Persistent cache: (state_key, TURN, depth, perspective) -> exact value.
# Persists across turns since a given hypothetical state's evaluation never changes.
TRANSPOSITION_TABLE = {}


def stateKey(ownedBy):
    # Tuple of owners in a fixed node order - hashable, cheap to build, cheap to compare.
    return tuple(ownedBy[n] for n in ALL_NODES_ORDERED)


def getBestMove(TURN, depth=8):
    ownedBy = {}
    for node in ALL_NODES:
        ownedBy[node] = node.owner

    p1Count = len(P1_TRIADS)
    p2Count = len(P2_TRIADS)

    options = getAvailableMovesSim(ownedBy, TURN)
    nextTurn = PLAYER_1 if TURN == PLAYER_2 else PLAYER_2

    bestMoves = []
    bestScore = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    for node in options:
        newOwnedBy, newP1, newP2 = simCapture(ownedBy, p1Count, p2Count, node, TURN)
        value = recursiveGetBest(newOwnedBy, newP1, newP2, nextTurn, depth - 1, TURN, alpha, beta)

        if value > bestScore:
            bestScore = value
            bestMoves = [node]
        elif value == bestScore:
            bestMoves.append(node)

        alpha = max(alpha, bestScore)

    return random.choice(bestMoves)


def recursiveGetBest(ownedBy, p1Count, p2Count, TURN, depth, perspective, alpha, beta):

    # --- Problem 1 fix: check depth before doing any move-generation work ---
    if depth == 0:
        return (p1Count - p2Count) if perspective == PLAYER_1 else (p2Count - p1Count)

    # --- transposition table lookup ---
    key = (stateKey(ownedBy), TURN, depth, perspective)
    cached = TRANSPOSITION_TABLE.get(key)
    if cached is not None:
        return cached

    options = getAvailableMovesSim(ownedBy, TURN)

    if len(options) == 0:
        value = (p1Count - p2Count) if perspective == PLAYER_1 else (p2Count - p1Count)
        TRANSPOSITION_TABLE[key] = value
        return value

    nextTurn = PLAYER_1 if TURN == PLAYER_2 else PLAYER_2
    isMaximizing = (TURN == perspective)

    pruned = False

    if isMaximizing:
        bestValue = -float('inf')
        for node in options:
            newOwnedBy, newP1, newP2 = simCapture(ownedBy, p1Count, p2Count, node, TURN)
            value = recursiveGetBest(newOwnedBy, newP1, newP2, nextTurn, depth - 1, perspective, alpha, beta)
            bestValue = max(bestValue, value)
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                pruned = True
                break
    else:
        bestValue = float('inf')
        for node in options:
            newOwnedBy, newP1, newP2 = simCapture(ownedBy, p1Count, p2Count, node, TURN)
            value = recursiveGetBest(newOwnedBy, newP1, newP2, nextTurn, depth - 1, perspective, alpha, beta)
            bestValue = min(bestValue, value)
            beta = min(beta, bestValue)
            if beta <= alpha:
                pruned = True
                break

    # Only cache exact values - a pruned branch's bestValue is a bound, not the true value,
    # so caching it could feed a wrong number into a later, differently-bounded search.
    if not pruned:
        TRANSPOSITION_TABLE[key] = bestValue

    return bestValue


def nodesOwnedBy(ownedBy, TURN):

    nodes = []
    for node in ownedBy.keys():
        if ownedBy[node] == TURN:
            nodes.append(node)

    return nodes


def getAvailableMovesSim(ownedBy, TURN):

    availableMoves = set()

    for node in nodesOwnedBy(ownedBy, TURN):
        for node2 in ADJACENCY[node]:
            if ownedBy[node2] == 0:
                availableMoves.add(node2)

        for same_name_node in NAME_LOOKUP[node.name]:
            if ownedBy[same_name_node] == 0:
                availableMoves.add(same_name_node)

    return availableMoves


def getScore(ownedBy):
    p1triads = set()
    p2triads = set()

    for node in ownedBy.keys():
        owner = ownedBy[node]
        if owner == 0:
            continue

        for node2 in ADJACENCY[node]:
            if ownedBy[node2] != owner:
                continue

            for node3 in ADJACENCY[node2]:
                if ownedBy[node3] != owner:
                    continue
                if node3 not in ADJACENCY[node]:
                    continue

                triad = frozenset({node, node2, node3})
                if owner == 1:
                    p1triads.add(triad)
                elif owner == 2:
                    p2triads.add(triad)

    return len(p1triads), len(p2triads)


def simCapture(ownedBy, p1Count, p2Count, node, turn):
    newOwned = dict(ownedBy)
    newOwned[node] = turn

    same_owner_neighbors = [n for n in ADJACENCY[node] if newOwned[n] == turn]
    newTriads = 0
    for i in range(len(same_owner_neighbors)):
        for j in range(i + 1, len(same_owner_neighbors)):
            a, b = same_owner_neighbors[i], same_owner_neighbors[j]
            if b in ADJACENCY[a]:
                newTriads += 1

    if turn == PLAYER_1:
        p1Count += newTriads
    else:
        p2Count += newTriads

    return newOwned, p1Count, p2Count