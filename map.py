from random import choices, randint, random

def generateMap(length=32, greediness = 0.1, branchChance = 0.75, textures = ([1, 2, 3], [25, 5, 1])):
    """
    Generates the map

    @param length: int - the side length of the square created
    
    @param greediness: float - how direct the path to the endpoint will be
    
    @param branchChance: float - how likely a branch is to further branch out
    
    @param textures: ([int], [int]) - a tuple containing a list of integers to represent textures, and a list with the weights
    
    @returns - a tuple containing the map as a 2d array, the starting point coordinates, and the endpoint coordinates
    """
    startTile = (1, randint(1, length - 2))
    endTile = (length - 2, randint(1, length - 2))

    map = [[choices(textures[0], weights=textures[1], k=1)[0] for i in range(length)] for j in range(length)]

    branchEnds = []
    emptyTiles = []

    # generate initial path
    lastTile = startTile
    while lastTile != endTile:
        surroundingTiles = getSurroundingTiles(lastTile[0], lastTile[1], (0, length - 1), (0, length - 1), map, invalid = 0)[0]
        weights = []

        if endTile in surroundingTiles:
            break

        for i in surroundingTiles:
            borderTiles = getSurroundingTiles(i[0], i[1], (0, length - 1), (0, length - 1), map, invalid=0)
            if borderTiles[1] > 1:
                weights.append(-1)
            else:
                weights.append(abs(endTile[0] - i[0]) + abs(endTile[1] - i[1]))

        if not len(surroundingTiles) or all([i == -1 for i in weights]): # we've dug ourselves into an area where it is impossible to continue without intersecting with our previous path
            # print(f"failed! {weights} {surroundingTiles}")
            map = [[choices(textures[0], weights=textures[1], k=1)[0] for i in range(length)] for j in range(length)]
            lastTile = startTile
            emptyTiles = []
            branchEnds = []
            continue
        
        highestWeight = max(weights) + 1
        
        for i, v in enumerate(weights):
            if v != -1:
                weights[i] = (highestWeight - v) ** greediness
            else:
                weights[i] = 0

        nextTile = choices(surroundingTiles, weights=weights, k=1)[0]
        map[nextTile[1]][nextTile[0]] = 0
        emptyTiles.append(nextTile)
        if random() < branchChance:
            branchEnds.append(nextTile)
        lastTile = nextTile

    
    map[endTile[1]][endTile[0]] = 0
    map[endTile[1]][endTile[0] + 1] = -2
    map[startTile[1]][startTile[0]] = 0
    map[startTile[1]][startTile[0] - 1] = -1

    # start branching out
    while len(branchEnds):
        branchEnd = branchEnds.pop(0)
        candidates = getSurroundingTiles(branchEnd[0], branchEnd[1], (0, length - 1), (0, length - 1), map, invalid=0)[0]

        for candidate in candidates:
            if getSurroundingTiles(candidate[0], candidate[1], (0, length - 1), (0, length - 1), map, invalid=0)[1] <= 1 and random() < branchChance:
                branchEnds.append(candidate)
                map[candidate[1]][candidate[0]] = 0
                emptyTiles.append(candidate)
    
    return (map, startTile, endTile, emptyTiles)

def getSurroundingTiles(x, y, boundX, boundY, map, invalid = None):
    out = []
    invalidTiles = 0

    if x + 1 < boundX[1]:
        if map[y][x + 1] != invalid:
            out.append((x + 1, y))
        else:
            invalidTiles += 1
    if x - 1 > boundX[0]:
        if map[y][x - 1] != invalid:
            out.append((x - 1, y))
        else:
            invalidTiles += 1
    if y + 1 < boundY[1]:
        if map[y + 1][x] != invalid:
            out.append((x, y + 1))
        else:
            invalidTiles += 1
    if y - 1 > boundY[0]:
        if map[y - 1][x] != invalid:
            out.append((x, y - 1))
        else:
            invalidTiles += 1
    return (out, invalidTiles)

localMap = generateMap(length=16, greediness=0.1, branchChance=0.75)
mapInfo = lambda: localMap
map = lambda: mapInfo()[0]

debugMap = [
    "black",
    "blue",
    "#42a7f5",
    "#950000",
    "red",
    "green"
]