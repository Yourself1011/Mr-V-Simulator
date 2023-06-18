from dotenv import load_dotenv
load_dotenv()

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
from platform import system
from eventHandlers import init as initEventHandlers, door

try: 
    from replit import db
except Exception as e:
    print(str(e) + "\nCouldn't connect to database, running in offline mode")
    db = {"highscore": ("", 0)}

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


def scoreboard(x, y, index, nameLength = 15, firstTime = False, inputScore=None, **kwargs):
    scores = highscores[index:index+5]
    if osName == "Darwin":
        screen.create_rectangle(
            x,
            y - 12 * 5,
            x + (nameLength + 2) * 12 + 6,
            y + 12 * 5,
            fill="gray50",
            outline="",
            tags=["scoreboard", "delete"]
        )

    else:
        screen.create_rectangle(
            x,
            y - 12 * 5,
            x + (nameLength + 2) * 12 + 6,
            y + 12 * 5,
            fill="",
            outline="",
            tags=["scoreboard", "delete"]
        )

    output = []
    for j, i in enumerate(scores):
        length = nameLength - len(str(j + index + 1))
        output.append(f"{j + index + 1}. {i[0] if len(i[0]) <= length else i[0][:length-3] + '...'}{' ' * (length - len(i[0]))}  {i[1]}")

    output = "\n".join(output)
    
    screen.create_text(
        x,
        y,
        text="Leaderboard (scroll):\n" + output,
        anchor=tkinter.W,
        font=("Dejavu Sans Mono", 12),
        tags=["scoreboard", "delete"],
        **kwargs
    )

    if inputScore and not submitted:
        if firstTime:
            screen.create_window(x + 55, y + 12 * 6, anchor=tkinter.W, window=nameInput, tags="score")
        screen.create_text(
            x,
            y + 12 * 6,
            anchor=tkinter.W,
            text="Name: ",
            font=("Dejavu Sans Mono", 12),
            fill="white",
            tags="score"
        )
        screen.create_rectangle(
            x + 190,
            y + 12 * 6 - 12,
            x + 260,
            y + 12 * 6 + 12,
            fill="gray75",
            stipple="gray75",
            tags=["scorebutton", "score"]
        )
        screen.create_text(
            x + 225,
            y + 12 * 6,
            text="Submit",
            fill="white",
            font=("Dejavu Sans", 11),
            tags=["scorebutton", "score"]
        )

        screen.tag_bind("scorebutton", "<Button-1>", lambda e: submitScore(inputScore))


def submitScore(inputScore):
    global highscores, submitted
    db["highscores"].append((nameInput.get(), inputScore))
    highscores = sorted(db["highscores"], key=lambda x: x[1], reverse=True)
    screen.delete("score")
    submitted=True

    
def deathScreen(index, firstTime = False):
    screen.delete("deleteOnDeath")
    if osName == "Darwin":
        screen.create_rectangle(
            screen.width / 2 - 175,
            screen.height / 4 - 100,
            screen.width / 2 + 175,
            screen.height / 4 + 100,
            fill="gray50"
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


def startGame(level = 0, reset=False):
    global f, sessionHighscore, submitted, index, totalF
    screen.delete("all")
    Sprite.instances = []
    player.dead = False
    submitted = False
    f = 1
    deadFrame = 0
    index = 0

    root.focus_set()
    screen.focus_set()
    
    start = time()

    if osName in ["Darwin"]:
        screen.bind("scoreboard", "<MouseWheel>", lambda e: updateIndex(-e.delta))
    elif osName in ["Windows"]:
        screen.bind("scoreboard", "<MouseWheel>", lambda e: updateIndex(-e.delta / 120))
    else:
        screen.tag_bind("scoreboard", "<Button-4>", lambda e: updateIndex(-1))
        screen.tag_bind("scoreboard", "<Button-5>", lambda e: updateIndex(1))

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
                
            
        if eventHandlers.mouse and not player.dead and f != 1:
            eventHandlers.mouse = False
            if f - player.loadFrame > 10:
                player.loadFrame = f
                if player.target:
                    player.target.deathFrame = f
                    player.score += level
                    sessionHighscore = max(sessionHighscore, player.score)
                    
        player.target = None
        renderFrame(player.rays, f, level)
        player.move()
        
        if player.dead:
            if not deadFrame:
                deathScreen(index, firstTime = True)
            else:
                deathScreen(index)

        # debug screen
        if debug:
            updateDebugScreen(totalF, start)
        
        screen.update()
        
        sleep(max(0, (start + 1 / fps * f) - time()))
        screen.delete("delete")
        f += 1
        totalF += 1
        if debug:
            screenD.delete("delete")

        if door() and not player.dead:
            eventHandlers.localDoor = False
            startGame(level + 1)

def firstStart():
    global osName, sessionHighscore, highscores, nameInput, totalF
    if "highscores" not in db.keys():
        db["highscores"] = [
            (" ", 0)
        ]
    
    initEventHandlers()
    osName = system()
    sessionHighscore = 0
    totalF = 1
    highscores = sorted(db["highscores"], key=lambda x: x[1], reverse=True)
    nameInput = tkinter.Entry(root, width=15)
    screen.tag_bind("startButton", "<Button-1>", lambda e: startGame(level=1, reset=True))
    startGame(reset=True)

root.after(100, firstStart)
root.mainloop()