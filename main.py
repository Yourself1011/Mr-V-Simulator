from dotenv import load_dotenv
load_dotenv()

from player import player
import consts
from consts import screen, root, debug, screenD, screenDScale, fps, fov, osName
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
import database
from database import scoreboard, highscores

def renderFrame(rays: list[Ray], f, intro=False):
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
    
        rayToSlice(i, ray, player, hit[0], textureMap[hit[2]], hit[1], level)

        # solid blue walls
        # screen.create_line(
        #     i,
        #     baseline - (1 - playerHeightPercent) * wallHeight,
        #     i,
        #     baseline + playerHeightPercent * wallHeight,
        #     fill="blue",
        #     width=1
        # )
    if not intro:

        # sprites
        for i in Sprite.instances:
            i.draw(player, rays, f, level)
    
        Sprite.instances.sort(key=lambda x: x.relDistance, reverse=True)
            
        # crosshair
        screen.create_line(
            screen.width // 2,
            screen.height // 2 - 10,
            screen.width // 2,
            screen.height // 2 + 10,
            fill="white",
            tags=["delete", "deleteOnDeath"]
        )
        screen.create_line(
            screen.width // 2 - 10,
            screen.height // 2,
            screen.width // 2 + 10,
            screen.height // 2,
            fill="white",
            tags=["delete", "deleteOnDeath"]
        )
    
        # stamp in hand
        if f - player.loadFrame > 10:
            screen.create_image(screen.width, screen.height, anchor=tkinter.SE, image=stamper, tags="delete")
    
        # score
        screen.create_text(
            screen.width - 15,
            15,
            anchor=tkinter.NE,
            text=f"Score: {player.score}\nHigh Score: {sessionHighscore}\nLevel: {level}",
            justify=tkinter.RIGHT,
            font=("Dejavu Sans", 30),
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


    
def deathScreen(index, firstTime = False):
    screen.delete("deleteOnDeath")
    if osName == "Darwin":
        screen.create_rectangle(
            screen.width / 2 - 175,
            screen.height / 4 - 100,
            screen.width / 2 + 175,
            screen.height / 4 + 100,
            fill="gray50",
            tags="delete"
        )
    
    else: 
        screen.create_rectangle(
            0,
            0,
            screen.width,
            screen.height,
            fill="black",
            stipple="gray75",
            tags="delete"
        )
    
    screen.create_text(
        screen.width / 2, 
        screen.height / 4, 
        anchor=tkinter.CENTER, 
        fill="white", 
        text=f"Game over!\nScore: {player.score}\nHigh Score: {sessionHighscore}", 
        justify="center", 
        tags="delete", 
        font=("Dejavu Sans", 36)
    )

    screen.create_rectangle(
        screen.width / 2 - 200,
        screen.height * 3 / 4 - 36,
        screen.width / 2 + 200,
        screen.height * 3 / 4 + 36,
        fill="gray75",
        stipple="gray75",
        tags=["delete", "startButton"]
    )
    screen.create_text(
        screen.width / 2,
        screen.height * 3 / 4,
        text="Restart",
        font=("Dejavu Sans", 36),
        anchor=tkinter.CENTER,
        fill="white",
        tags=["delete", "startButton"]
    )

    scoreboard(25, screen.height / 4, index, firstTime=firstTime, inputScore=player.score, fill="white")


def updateIndex(amount):
    global index
    index = max(min(index + amount, len(highscores) - 5), 0)

def pauseMenu(index):
    screen.tag_bind("optionsButton", "<Button-1>", lambda e: optionsScreen(lambda: pauseMenu(index)))

    while eventHandlers.paused:
        renderFrame(player.rays, f)
        if osName == "Darwin":
            screen.create_rectangle(
                screen.width / 2 - 175,
                screen.height / 4 - 100,
                screen.width / 2 + 175,
                screen.height / 4 + 100,
                fill="gray50",
                tags="delete"
            )
        
        else: 
            screen.create_rectangle(
                0,
                0,
                screen.width,
                screen.height,
                fill="black",
                stipple="gray75",
                tags="delete"
            )
        
        screen.create_text(
            screen.width / 2, 
            screen.height / 4, 
            anchor=tkinter.CENTER, 
            fill="white", 
            text=f"Game paused\nScore: {player.score}\nHigh Score: {sessionHighscore}", 
            justify="center", 
            tags="delete", 
            font=("Dejavu Sans", 36)
        )
        
        screen.create_rectangle(
            screen.width / 2 - 200,
            screen.height * 9 / 16 - 36,
            screen.width / 2 + 200,
            screen.height * 9 / 16 + 36,
            fill="gray75",
            stipple="gray75",
            tags=["delete", "optionsButton"]
        )
        screen.create_text(
            screen.width / 2,
            screen.height * 9 / 16,
            text="Options",
            font=("Dejavu Sans", 36),
            anchor=tkinter.CENTER,
            fill="white",
            tags=["delete", "optionsButton"]
        )
    
        screen.create_rectangle(
            screen.width / 2 - 200,
            screen.height * 3 / 4 - 36,
            screen.width / 2 + 200,
            screen.height * 3 / 4 + 36,
            fill="gray75",
            stipple="gray75",
            tags=["delete", "resumeButton"]
        )
        screen.create_text(
            screen.width / 2,
            screen.height * 3 / 4,
            text="Resume",
            font=("Dejavu Sans", 36),
            anchor=tkinter.CENTER,
            fill="white",
            tags=["delete", "resumeButton"]
        )
    
        scoreboard(25, screen.height / 4, index, fill="white")
        screen.update()
        sleep(0.1)
        if eventHandlers.paused:
            screen.delete("delete")


def optionsScreen(returnFunction):
    running = True

    def updateGraphics(value, returnFunction):
        nonlocal running
        running = False
        consts.precision = value
        player.rays = [Ray(fov / screen.width * i - fov / 2) for i in range(0, screen.width, consts.getVerticalPrecision())]
        screen.delete("delete")
        optionsScreen(returnFunction)
        
    def handleReturn():
        nonlocal running
        running = False
        returnFunction()
    
    screen.tag_bind("returnButton", "<Button-1>", lambda e: handleReturn())
    screen.tag_bind("graphicsButton", "<Button-1>", lambda e: updateGraphics((consts.precision + 1) % len(consts.precisionPresets), returnFunction))

    while running:
        renderFrame(player.rays, 0, intro=True)
        
        if osName == "Darwin":
            screen.create_rectangle(
                screen.width / 2 - 175,
                screen.height / 4 - 30,
                screen.width / 2 + 175,
                screen.height / 4 + 30,
                fill="gray50",
                tags="delete"
            )
        
        else: 
            screen.create_rectangle(
                0,
                0,
                screen.width,
                screen.height,
                fill="black",
                stipple="gray75",
                tags="delete"
            )
        
        screen.create_text(
            screen.width / 2, 
            screen.height / 4, 
            anchor=tkinter.CENTER, 
            fill="white", 
            text="Options", 
            justify="center", 
            tags="delete", 
            font=("Dejavu Sans", 36)
        )
           
        screen.create_rectangle(
            screen.width / 2 - 400,
            screen.height * 9 / 16 - 36,
            screen.width / 2 + 400,
            screen.height * 9 / 16 + 36,
            fill="gray75",
            stipple="gray75",
            tags=["delete", "graphicsButton"]
        )
        screen.create_text(
            screen.width / 2,
            screen.height * 9 / 16,
            text=f"Graphics: {list(consts.precisionPresets.keys())[consts.precision]}",
            font=("Dejavu Sans", 36),
            anchor=tkinter.CENTER,
            fill="white",
            tags=["delete", "graphicsButton"]
        )
            
        screen.create_rectangle(
            screen.width / 2 - 200,
            screen.height * 3 / 4 - 36,
            screen.width / 2 + 200,
            screen.height * 3 / 4 + 36,
            fill="gray75",
            stipple="gray75",
            tags=["delete", "returnButton"]
        )
        screen.create_text(
            screen.width / 2,
            screen.height * 3 / 4,
            text="Return",
            font=("Dejavu Sans", 36),
            anchor=tkinter.CENTER,
            fill="white",
            tags=["delete", "returnButton"]
        )

        screen.update()
        sleep(0.1)
        if running:
            screen.delete("delete")

def introScreen():
    global osName, index, level

    screen.tag_bind("firstStartButton", "<Button-1>", lambda e: firstStart())
    screen.tag_bind("optionsButton", "<Button-1>", lambda e: optionsScreen(introScreen))

    if osName in ["Darwin"]:
        screen.bind("scoreboard", "<MouseWheel>", lambda e: updateIndex(-e.delta))
    elif osName in ["Windows"]:
        screen.bind("scoreboard", "<MouseWheel>", lambda e: updateIndex(-e.delta / 120))
    else:
        screen.tag_bind("scoreboard", "<Button-4>", lambda e: updateIndex(-1))
        screen.tag_bind("scoreboard", "<Button-5>", lambda e: updateIndex(1))
    
    map.localMap = generateMap()
    mapInfo = map.mapInfo()
    player.x = mapInfo[1][0] * 64 + 8
    player.y = mapInfo[1][1] * 64 + 32
    player.toRotate = 0.5
    level = 0
    f = 0
    index = 0
    
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
        renderFrame(player.rays, f, intro=True)

        if osName == "Darwin":
            screen.create_rectangle(
                screen.width / 2 - 200,
                screen.height / 4 - 30,
                screen.width / 2 + 200,
                screen.height / 4 + 30,
                fill="gray50",
                tags="delete"
            )
            screen.create_rectangle(
                screen.width * 7 / 8 - 100,
                screen.height / 4 - 30,
                screen.width * 7 / 8 + 100,
                screen.height / 4 + 30,
                fill="gray50",
                tags="delete"
            )
        
        else: 
            screen.create_rectangle(
                0,
                0,
                screen.width,
                screen.height,
                fill="black",
                stipple="gray75",
                tags="delete"
            )
        
        screen.create_text(
            screen.width / 2, 
            screen.height / 4, 
            anchor=tkinter.CENTER, 
            fill="white", 
            text="Mr. V Simulator", 
            justify="center", 
            tags="delete", 
            font=("Dejavu Sans", 36)
        )

        screen.create_text(
            screen.width * 7 / 8,
            screen.height / 4,
            anchor = tkinter.CENTER,
            justify = tkinter.CENTER,
            text="WASD\nMouse to rotate",
            tags="delete",
            fill="white",
            font=("Dejavu Sans", 12)
        )
            
        screen.create_rectangle(
            screen.width / 2 - 200,
            screen.height * 9 / 16 - 36,
            screen.width / 2 + 200,
            screen.height * 9 / 16 + 36,
            fill="gray75",
            stipple="gray75",
            tags=["delete", "optionsButton"]
        )
        screen.create_text(
            screen.width / 2,
            screen.height * 9 / 16,
            text="Options",
            font=("Dejavu Sans", 36),
            anchor=tkinter.CENTER,
            fill="white",
            tags=["delete", "optionsButton"]
        )
    
        screen.create_rectangle(
            screen.width / 2 - 200,
            screen.height * 3 / 4 - 36,
            screen.width / 2 + 200,
            screen.height * 3 / 4 + 36,
            fill="gray75",
            stipple="gray75",
            tags=["delete", "firstStartButton"]
        )
        screen.create_text(
            screen.width / 2,
            screen.height * 3 / 4,
            text="Start game",
            font=("Dejavu Sans", 36),
            anchor=tkinter.CENTER,
            fill="white",
            tags=["delete", "firstStartButton"]
        )
    
        scoreboard(25, screen.height / 4, index, fill="white")
        screen.update()
        sleep(0.1)
        screen.delete("delete")
        f += 1

def startGame(levelParam, reset=False):
    global f, sessionHighscore, index, totalF, level
    level = levelParam
    
    screen.delete("all")
    Sprite.instances = []
    player.dead = False
    database.submitted = False
    f = 1
    deadFrame = 0
    index = 0

    if reset:
        # root.focus_set()
        screen.focus_set()
    eventHandlers.paused = False
    
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
        
    while True:
        if player.dead:

            if not deadFrame:
                deadFrame = f
                deathStartAngle = player.rot
                interval = player.deathSprite.relAngle
                player.toRotate = 0
                player.moveKeys = []

            if 5 < f - deadFrame <= 15:
                player.rot = deathStartAngle + interval * ((f - 5 - deadFrame) / 10)
                
            
        if eventHandlers.mouse and not player.dead and not eventHandlers.paused and f != 1:
            eventHandlers.mouse = False
            if f - player.loadFrame > 10:
                player.loadFrame = f
                if player.target:
                    player.target.deathFrame = f
                    player.score += level
                    sessionHighscore = max(sessionHighscore, player.score)
                    
        if eventHandlers.paused and f != 1:
            player.toRotate = 0
            player.moveKeys = []
        player.target = None
        renderFrame(player.rays, f)
        player.move()
        
        if player.dead:
            if not deadFrame:
                deathScreen(index, firstTime = True)
            else:
                deathScreen(index)

        elif eventHandlers.paused:
            pauseMenu(index)
  
        # debug screen
        if debug:
            updateDebugScreen(totalF, start)
        
        screen.update()
        
        sleep(max(0, (start + 1 / fps * f) - time()))
        totalF += 1
        if not eventHandlers.paused:
            f += 1
        screen.delete("delete")
        if debug:
            screenD.delete("delete")

        if door() and not player.dead and not eventHandlers.paused:
            eventHandlers.localDoor = False
            startGame(level + 1)

def firstStart():
    global sessionHighscore, totalF
    
    initEventHandlers()
    sessionHighscore = 0
    totalF = 1
    screen.tag_bind("startButton", "<Button-1>", lambda e: startGame(1, reset=True))
    startGame(0, reset=True)

root.after(100, introScreen)
root.mainloop()