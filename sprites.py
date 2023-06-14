from consts import fov, debug, screenD, screenDScale
from math import atan, degrees, sqrt, radians, cos, floor, tan
from assets import spriteTextureMap
from raycaster import rayToSlice
from map import mapInfo, map
from random import choice, uniform

class Sprite:
    instances = []
    def __init__(self, x, y, width, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.sprite = sprite
        self.__class__.instances.append(self)
        
    def draw(self, player, rays):
        if debug:
            screenD.create_oval(
                self.x * screenDScale - self.width * screenDScale / 2,
                self.y * screenDScale - self.width * screenDScale / 2,
                self.x * screenDScale + self.width * screenDScale / 2,
                self.y * screenDScale + self.width * screenDScale / 2,
                fill="green"
            )
        
        deltaY = player.y - self.y
        deltaX = player.x - self.x
        relDistance = sqrt(deltaX ** 2 + deltaY ** 2)
        if deltaY == 0:
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

        interval = fov / len(rays)

        currentAngle = max(min(fov / 2, degrees(atan(self.width / 2 / relDistance)) - relAngle), -fov / 2)
        minAngle = min(max(-fov / 2, degrees(atan(-self.width / 2 / relDistance)) - relAngle), fov / 2)

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
            sliceDepth = relDistance / cos(radians(currentAngle + relAngle))
            hitLocation = relDistance * tan(radians(currentAngle + relAngle))
            
            if abs(ray.length) > abs(sliceDepth):
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
    def __init__(self, speed):
        lastSquare = choice(mapInfo[3])
        coords = lastSquare
        
        super().__init__(*[i * 64 + 32 for i in coords], 64, 1)

    def draw(self, player, rays):
        
        super().draw(player, rays)

for i in range(10):
    Assignment(uniform(8, 16))