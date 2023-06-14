from player import player
from consts import screen, root, debug, screenD, screenDScale, fps, fov
from raycaster import Ray, rayToSlice
import map
from map import debugMap, generateMap
from math import sin, cos, radians
from sprites import Sprite
from assets import textureMap
from time import sleep, time
from random import uniform
import tkinter
from eventHandlers import init as initEventHandlers

def renderFrame(rays: list[Ray]):
    # playerHeightPercent = player.z / 64
    # baseline = screen.height - screen.height * playerHeightPercent

    # floor
    screen.create_rectangle(
        0,
        screen.height // 2,
        screen.width,
        screen.height,
        fill="gray",
        tags="delete"
    )
    
    for i, ray in enumerate(rays):    
        hit = ray.getNearestWall(player.rot, player.x, player.y)
    
        rayToSlice(i, ray, player, hit[0], textureMap[hit[2]], hit[1])

        # solid blue walls
        # screen.create_line(
        #     i,
        #     baseline - (1 - playerHeightPercent) * wallHeight,
        #     i,
        #     baseline + playerHeightPercent * wallHeight,
        #     fill="blue",
        #     width=1
        # )
        
    # crosshair
    screen.create_line(
        screen.width // 2,
        screen.height // 2 - 10,
        screen.width // 2,
        screen.height // 2 + 10,
        fill="white",
        tags="delete"
    )
    screen.create_line(
        screen.width // 2 - 10,
        screen.height // 2,
        screen.width // 2 + 10,
        screen.height // 2,
        fill="white",
        tags="delete"
    )

    # sprites
    for i in Sprite.instances:
        i.draw(player, rays)

def updateDebugScreen(f, start):
    screenD.create_text(10, 10, fill="white", anchor = tkinter.NW, text=f"{f / (time() - start) }\n{player.rot}\n{player.x}\n{player.y}", tags="delete")

    screenD.create_line(
        player.x * screenDScale,
        player.y * screenDScale,
        (player.x + sin(radians(player.rot)) * 50) * screenDScale,
        (player.y + cos(radians(player.rot)) * 50) * screenDScale,
        fill="white",
        tags="delete"
    )
    screenD.create_line(
        player.x * screenDScale,
        player.y * screenDScale,
        (player.x + sin(radians(player.rot + fov/2)) * 50) * screenDScale,
        (player.y + cos(radians(player.rot + fov/2)) * 50) * screenDScale,
        fill="white",
        tags="delete"
    )
    screenD.create_line(
        player.x * screenDScale,
        player.y * screenDScale,
        (player.x + sin(radians(player.rot - fov/2)) * 50) * screenDScale,
        (player.y + cos(radians(player.rot - fov/2)) * 50) * screenDScale,
        fill="white",
        tags="delete"
    )
    
    screenD.create_oval(
        player.x * screenDScale + 10,
        player.y * screenDScale + 10,
        player.x * screenDScale - 10,
        player.y * screenDScale - 10,
        fill="yellow",
        tags = "delete"
    )

def startGame():
    initEventHandlers()
    f = 1
    start = time()
    
    if debug:
        gridLength = screenD.length / len(map.map)
        for r, i in enumerate(map.map):
            for c, j in enumerate(i):
                screenD.create_rectangle(
                    c * gridLength,
                    r * gridLength,
                    c * gridLength + gridLength,
                    r * gridLength + gridLength,
                    fill=debugMap[j]
                )

    # sky
    for i in range(100):
        x = uniform(0, screen.width)
        y = uniform(0, screen.height / 2)
        size = uniform(2, 4)

        screen.create_oval(
            x,
            y,
            x + size,
            y + size,
            outline="",
            fill="white"
        )
        
    while True:
        player.move()
        renderFrame(player.rays)

        # debug screen
        if debug:
            updateDebugScreen(f, start)
        
        screen.update()
        sleep(max(0, (start + 1 / fps * f) - time()))
        screen.delete("delete")
        f += 1
        if debug:
            screenD.delete("delete")

        if f == 20:
            print("hi")
            map.mapInfo = generateMap(length=16, greediness=0.1, branchChance=0.75)
            map.map = map.mapInfo[0]

root.after(100, startGame)
root.mainloop()