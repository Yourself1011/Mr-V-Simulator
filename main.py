from player import player
import consts
from consts import screen, root, debug, screenD, screenDScale, fps, fov
from raycaster import Ray, rayToSlice
import map
from map import debugMap, generateMap, mapInfo
from math import sin, cos, radians, log, floor
from sprites import Sprite, Assignment
from assets import textureMap, stamper
from time import sleep, time
from random import uniform
import tkinter
import eventHandlers
from eventHandlers import init as initEventHandlers, door

def renderFrame(rays: list[Ray], f, level):
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

    # sprites
    for i in Sprite.instances:
        i.draw(player, rays, f)

    Sprite.instances.sort(key=lambda x: x.relDistance, reverse=True)
        
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

    # stamp in hand
    if f - player.loadFrame > 10:
        screen.create_image(screen.width, screen.height, anchor=tkinter.SE, image=stamper, tags="delete")

    # score
    screen.create_text(
        screen.width - 15,
        15,
        anchor=tkinter.NE,
        text=f"Score: {player.score}\nLevel: {level}",
        justify=tkinter.RIGHT,
        font=("Dejavu Sans", 40),
        fill="white",
        tags=["delete", "deleteOnDeath"]
    )

    
    if round(player.x / 64) == mapInfo()[2][0] + 1 and floor(player.y / 64) == mapInfo()[2][1]:
        screen.create_text(
            screen.width / 2,
            screen.height / 2 - 10,
            text="Press E to enter",
            fill="white",
            font=("Dejavu Sans", 20),
            anchor=tkinter.S,
            tags=["delete", "deleteOnDeath"]
        )

def updateDebugScreen(f, start):
    screenD.create_text(10, 10, fill="white", anchor = tkinter.NW, text=f"{f / (time() - start) }\n{player.rot}\n{player.x}\n{player.y}", tags="delete")

    screenD.create_line(
        player.x * screenDScale(),
        player.y * screenDScale(),
        (player.x + sin(radians(player.rot)) * 50) * screenDScale(),
        (player.y + cos(radians(player.rot)) * 50) * screenDScale(),
        fill="white",
        tags="delete"
    )
    screenD.create_line(
        player.x * screenDScale(),
        player.y * screenDScale(),
        (player.x + sin(radians(player.rot + fov/2)) * 50) * screenDScale(),
        (player.y + cos(radians(player.rot + fov/2)) * 50) * screenDScale(),
        fill="white",
        tags="delete"
    )
    screenD.create_line(
        player.x * screenDScale(),
        player.y * screenDScale(),
        (player.x + sin(radians(player.rot - fov/2)) * 50) * screenDScale(),
        (player.y + cos(radians(player.rot - fov/2)) * 50) * screenDScale(),
        fill="white",
        tags="delete"
    )
    
    screenD.create_oval(
        player.x * screenDScale() + 10,
        player.y * screenDScale() + 10,
        player.x * screenDScale() - 10,
        player.y * screenDScale() - 10,
        fill="yellow",
        tags = "delete"
    )

def deathScreen():
    screen.delete("deleteOnDeath")
    screen.create_rectangle(
        0,
        0,
        screen.width,
        screen.height,
        fill="gray",
        stipple="gray50",
        tags="delete"
    )
    
    screen.create_text(
        screen.width / 2, 
        screen.height / 4, 
        anchor=tkinter.CENTER, 
        fill="white", 
        text=f"Game over!\nScore: {player.score}", 
        justify="center", 
        tags="delete", 
        font=("Dejavu Sans", 40)
    )

    screen.create_rectangle(
        screen.width / 2 - 200,
        screen.height * 3 / 4 - 40,
        screen.width / 2 + 200,
        screen.height * 3 / 4 + 40,
        fill="gray",
        stipple="gray75",
        tags=["delete", "startButton"]
    )
    screen.create_text(
        screen.width / 2,
        screen.height * 3 / 4,
        text="Restart",
        font=("Dejavu Sans", 40),
        anchor=tkinter.CENTER,
        fill="white",
        tags=["delete", "startButton"]
    )
    

def startGame(level = 0, reset=False):
    global f
    Sprite.instances = []
    player.dead = False
    f = 1
    start = time()

    if debug:
        consts.localScreenDScale = screenD.length / (64 * round(5 * log(level + 0.1, 10) + 13))

    # Generate the map
    map.localMap = generateMap(
        length = round(5 * log(level + 0.1, 10) + 13), 
        greediness = 1 / (level + 0.3) - 0.1, 
        branchChance = -1 / (level + 0.25) + 0.9
    )
    mapInfo = map.mapInfo()
    if reset:
        player.score = 0
    player.loadFrame = -10
    player.x = mapInfo[1][0] * 64 + 8
    player.y = mapInfo[1][1] * 64 + 32
    
    # Put enimies
    for i in range(round(len(mapInfo[3]) * (-1/(0.75 * level + 3.45) + 0.3))):
        Assignment(uniform(4, 8), 0)
    
    if debug:
        gridLength = screenD.length / len(map.map())
        for r, i in enumerate(map.map()):
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
        
    while not player.dead:
        if eventHandlers.mouse:
            eventHandlers.mouse = False
            if f - player.loadFrame > 10:
                player.loadFrame = f
                if player.target:
                    player.target.deathFrame = f
                    player.score += level
                    
        player.target = None
        renderFrame(player.rays, f, level)
        player.move()

        # debug screen
        if debug:
            updateDebugScreen(f, start)
        
        screen.update()
        # if f == 20:
        #     print("hi")
        #     break
        if not player.dead:
            sleep(max(0, (start + 1 / fps * f) - time()))
            screen.delete("delete")
            f += 1
            if debug:
                screenD.delete("delete")

        if door():
            eventHandlers.localDoor = False
            startGame(level + 1)

    deathScreen()

def firstStart():
    initEventHandlers()
    screen.tag_bind("startButton", "<Button-1>", lambda e: startGame(level=1, reset=True))
    startGame(reset=True)

root.after(100, firstStart)
root.mainloop()