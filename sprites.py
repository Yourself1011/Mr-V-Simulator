from consts import fov, debug, screenD, screenDScale
from math import atan, degrees, sqrt, radians, cos, floor, tan
from assets import spriteTextureMap
from raycaster import rayToSlice
from map import mapInfo, map
from random import choice

class Sprite:
    instances = []
    def __init__(self, x, y, width, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.sprite = sprite
        self.relDistance = 0
        self.targetable = False
        self.__class__.instances.append(self)
        
    def draw(self, player, rays):
        if debug:
            screenD.create_oval(
                self.x * screenDScale - self.width * screenDScale / 2,
                self.y * screenDScale - self.width * screenDScale / 2,
                self.x * screenDScale + self.width * screenDScale / 2,
                self.y * screenDScale + self.width * screenDScale / 2,
                fill="green",
                tags="delete"
            )
        
        deltaY = player.y - self.y
        deltaX = player.x - self.x
        self.relDistance = sqrt(deltaX ** 2 + deltaY ** 2)
        if deltaY == 0 or deltaX == 0:
            relAngle = 90
            
        elif deltaY < 0 and deltaX < 0:
            relAngle = degrees(atan(abs(deltaX) / abs(deltaY)))

        elif deltaY > 0 and deltaX < 0:
            relAngle = degrees(atan(abs(deltaY) / abs(deltaX))) + 90
            
        elif deltaY > 0 and deltaX > 0:
            relAngle = degrees(atan(abs(deltaX) / abs(deltaY))) + 180
            
        else:
            relAngle = degrees(atan(abs(deltaY) / abs(deltaX))) + 270

        
        relAngle -= player.rot

        if relAngle < -180:
            relAngle = 360 + relAngle

        if relAngle > 180:
            relAngle = relAngle - 360

        # spread = atan(self.width / 2 / self.relDistance)
        # if self.targetable and -spread < relAngle < spread and (not player.target or self.relDistance < player.target.relDistance):
        #     player.targets = self
        #     print("target acquired")

        interval = fov / len(rays)

        currentAngle = max(min(fov / 2, degrees(atan(self.width / 2 / self.relDistance)) - relAngle), -fov / 2)
        minAngle = min(max(-fov / 2, degrees(atan(-self.width / 2 / self.relDistance)) - relAngle), fov / 2)

        # print(currentAngle, minAngle)

        # Bring to nearest ray's angle
        currentAngle = interval * round(currentAngle / interval)

        if currentAngle < minAngle:
            interval *= -1

        initialCondition = currentAngle > minAngle

        while initialCondition == (currentAngle > minAngle) and currentAngle != minAngle:
            index = floor((currentAngle + fov / 2) / (fov / (len(rays) - 1)))
            if index < 0 or index >= len(rays):
                print(index, len(rays), relAngle, currentAngle, minAngle)
            ray = rays[index]
            sliceDepth = self.relDistance / cos(radians(currentAngle + relAngle))
            hitLocation = self.relDistance * tan(radians(currentAngle + relAngle))
            
            if abs(ray.length) > abs(sliceDepth):
                if index == floor((fov / 2) / (fov / (len(rays) - 1))):
                    player.target = self
                
                rayToSlice(index, ray, player, sliceDepth, spriteTextureMap[self.sprite], hitLocation + self.width / 2)

                if debug:
                    screenD.create_line(
                        player.x * screenDScale,
                        player.y * screenDScale,
                        ray.endX * screenDScale,
                        ray.endY * screenDScale,
                        fill="white",
                        tags="delete"
                    )
                    
                    screenD.create_oval(
                        self.x * screenDScale - self.width * screenDScale / 2,
                        self.y * screenDScale - self.width * screenDScale / 2,
                        self.x * screenDScale + self.width * screenDScale / 2,
                        self.y * screenDScale + self.width * screenDScale / 2,
                        fill="orange",
                        tags="delete"
                    )

            # else:
            #     if debug:
            #         screenD.create_line(
            #             player.x * screenDScale,
            #             player.y * screenDScale,
            #             ray.endX * screenDScale,
            #             ray.endY * screenDScale,
            #             fill="orange",
            #             tags="delete"
            #         )
        
            currentAngle -= interval

class Assignment(Sprite):
    def __init__(self, speed, f):
        self.lastSquare = list(choice(mapInfo()[3]))
        self.coords = self.lastSquare.copy()
        self.speed = speed
        self.direction = None
        self.moveStartFrame = f
        self.deathFrame = None
        
        super().__init__(*[i * 64 + 32 for i in self.coords], 64, 1)
        self.targetable = True

    def draw(self, player, rays, f):
        if not self.deathFrame:
            # move
            if (self.direction == None or f - self.moveStartFrame > self.speed):
                # decide a new direction to go
                directions = []
                mapArray = map()
                if not mapArray[self.coords[1]][self.coords[0] + 1]:
                    directions.append(("right", [self.coords[0] + 1, self.coords[1]]))
                if not mapArray[self.coords[1]][self.coords[0] - 1]:
                    directions.append(("left", [self.coords[0] - 1, self.coords[1]]))
                if not mapArray[self.coords[1] + 1][self.coords[0]]:
                    directions.append(("down", [self.coords[0], self.coords[1] + 1]))
                if not mapArray[self.coords[1] - 1][self.coords[0]]:
                    directions.append(("up", [self.coords[0], self.coords[1] - 1]))
    
                if len(directions) > 1:
                    for i in directions:
                        if i[1] == self.lastSquare:
                            directions.remove(i)
                            break
    
                # print(directions)
                
                self.lastSquare = self.coords.copy()
                self.direction = choice(directions)[0]
                match self.direction:
                    case "right":
                        self.coords[0] += 1
                    case "left":
                        self.coords[0] -= 1
                    case "down":
                        self.coords[1] += 1
                    case "up":
                        self.coords[1] -= 1
                self.moveStartFrame = f - 1
    
            amount = (f - self.moveStartFrame) / self.speed
            match self.direction:
                case "right":
                    self.x = (self.lastSquare[0] + amount) * 64 + 32
                case "left":
                    self.x = (self.lastSquare[0] - amount) * 64 + 32
                case "down":
                    self.y = (self.lastSquare[1] + amount) * 64 + 32
                case "up":
                    self.y = (self.lastSquare[1] - amount) * 64 + 32

        else:
            if f - self.deathFrame > 6:
                self.instances.remove(self)
            elif f - self.deathFrame > 3:
                self.sprite = 3
            else:
                self.sprite = 2
        
        super().draw(player, rays)

# Assignment(2, 0)