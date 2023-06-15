from consts import screen
from player import player, angles
from math import floor
from map import mapInfo

mouse = False
localDoor = False
door = lambda: localDoor

def onKeyDown(e):
    global localDoor
    if e.keysym.lower() in angles.keys() and e.keysym not in player.moveKeys:
        player.moveKeys.append(e.keysym.lower())

    if e.keysym in ["Shift_L", "Shift_R"]:
        player.crouch = True
        player.z -= 16

    if e.keysym.lower() == "e":
        if round(player.x / 64) == mapInfo()[2][0] + 1 and floor(player.y / 64) == mapInfo()[2][1]:
            localDoor = True

def onKeyUp(e):
    if e.keysym in angles.keys():
        player.moveKeys.remove(e.keysym)

    if e.keysym in ["Shift_L", "Shift_R"]:
        player.crouch = False
        player.z += 16

def onMouseMove(e):
    player.toRotate = e.x / screen.width * 2 - 1
    player.toRotate = player.toRotate ** 2 if player.toRotate > 0 else -(player.toRotate ** 2)

def onMousePress(e):
    global mouse
    mouse = True

def init():
    screen.bind("<Key>", onKeyDown)
    screen.bind("<KeyRelease>", onKeyUp)
    screen.bind("<Motion>", onMouseMove)
    screen.bind("<Button-1>", onMousePress)
