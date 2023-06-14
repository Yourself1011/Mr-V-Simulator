from consts import screen
from player import player, angles


def onKeyDown(e):
    if e.keysym in angles.keys() and e.keysym not in player.moveKeys:
        player.moveKeys.append(e.keysym)

    if e.keysym in ["Shift_L", "Shift_R"]:
        player.crouch = True
        player.z -= 16

def onKeyUp(e):
    if e.keysym in angles.keys():
        player.moveKeys.remove(e.keysym)

    if e.keysym in ["Shift_L", "Shift_R"]:
        player.crouch = False
        player.z += 16

def onMouseMove(e):
    player.toRotate = e.x / screen.width * 2 - 1

def init():
    screen.bind("<Key>", onKeyDown)
    screen.bind("<KeyRelease>", onKeyUp)
    screen.bind("<Motion>", onMouseMove)

