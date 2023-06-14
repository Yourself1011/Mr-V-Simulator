from map import map
from math import floor, ceil, tan, radians, sqrt, cos
from consts import debug, screenD, screenDScale, screen, verticalPrecision, horizontalPrecision
from colourUtils import rgbToHex

class Ray:
    def __init__(self, angle):
        self.angle = angle
        self.length = 0
        self.endX = 0
        self.endY = 0
        
    def getNearestWall(self, offsetAngle, originX, originY):
        absAngle = (self.angle - offsetAngle + 180) % 360
        relAngle = self.angle % 360
        
        # vertical walls
        vertLength = 999999
        if absAngle != 180 and absAngle != 0:
            innerAngle = radians(((self.angle - offsetAngle) - 90) % 360)
            offsetRunVert = (floor(originX/64) - originX/64) * 64 if absAngle > 180 else (ceil(originX/64) - originX/64)*64
            offsetRiseVert = offsetRunVert * tan(innerAngle)
            # print(offsetRunVert, offsetRiseVert, originX, self.angle)
            
            runVert = -64 if absAngle > 180 else 64
            totalRunVert = offsetRunVert
            totalRiseVert = offsetRiseVert
            while True:
                indexYVert = floor((totalRiseVert + originY) / 64)
                indexXVert = (totalRunVert + originX) / 64 - 1 if absAngle > 180 else (totalRunVert + originX) / 64
                
                # print(indexY, indexX, runVert, totalRiseVert, totalRunVert, absAngle, degrees(innerAngle))
                
                if (indexYVert < 0 or indexYVert >= len(map)) or map[indexYVert][int(indexXVert)]:
                    break

                totalRunVert += runVert
                totalRiseVert = totalRunVert * tan(innerAngle)
            
            vertLength = sqrt(totalRunVert ** 2 + totalRiseVert ** 2)

        # Horizontal walls
        
        horLength = 999999
        if absAngle != 90 and absAngle != 270:
            innerAngle = radians(-(self.angle - offsetAngle) % 360)
            offsetRiseHor = (ceil(originY/64) - originY/64)*64 if absAngle > 90 and absAngle < 270 else (floor(originY/64) - originY/64)*64
            offsetRunHor = offsetRiseHor * tan(innerAngle)

            riseHor = 64 if absAngle > 90 and absAngle < 270 else -64
            totalRiseHor = offsetRiseHor
            totalRunHor = offsetRunHor
            while True:
                indexXHor = floor((totalRunHor + originX) / 64)
                indexYHor = (totalRiseHor + originY) / 64 if absAngle > 90 and absAngle < 270 else (totalRiseHor + originY) / 64 - 1

                # if absAngle < 90:
                #     print(indexY, indexX, riseHor, totalRiseHor, totalRunHor, self.angle, absAngle)
                
                if (indexXHor < 0 or indexXHor >= len(map[0])) or map[int(indexYHor)][indexXHor]:
                    break
                    
                totalRiseHor += riseHor
                totalRunHor = totalRiseHor * tan(innerAngle)
            
            horLength = sqrt(totalRunHor ** 2 + totalRiseHor ** 2)

        # print(vertLength, horLength, absAngle)
        if debug:
            if vertLength < horLength:
                screenD.create_line(
                    originX * screenDScale,
                    originY * screenDScale,
                    (originX + totalRunVert) * screenDScale,
                    (originY + totalRiseVert) * screenDScale,
                    fill="purple",
                    tags="delete"
                )
                self.endX = (originX + totalRunVert)
                self.endY = (originY + totalRiseVert)
            else:
                screenD.create_line(
                            originX * screenDScale,
                            originY * screenDScale,
                            (originX + totalRunHor) * screenDScale,
                            (originY + totalRiseHor) * screenDScale,
                            fill="red",
                            tags="delete"
                        )
                self.endX = (originX + totalRunHor)
                self.endY = (originY + totalRiseHor)
        self.length = min(vertLength, horLength) * cos(radians(relAngle)) #remove fisheye effect
        return (
            self.length,
            totalRiseVert + originY if vertLength < horLength else totalRunHor + originX,
            map[indexYVert][int(indexXVert)] if vertLength < horLength else map[int(indexYHor)][indexXHor]
        )

def rayToSlice(i, ray, player, distance, texture, hitLocation):
    playerHeightPercent = player.z / 64
    baseline = screen.height - screen.height * playerHeightPercent
    pixelHeight = 64 * screen.depth / distance / texture[1]
    top = baseline - (1 - playerHeightPercent) * pixelHeight * texture[1]

    for j in range(0, texture[1], horizontalPrecision):
        pixel = texture[0][floor(hitLocation % 64 * (texture[1] / 64))][j]
        if pixel[3] != 0:
            screen.create_rectangle(
                i * verticalPrecision,
                top + pixelHeight * j,
                i * verticalPrecision + verticalPrecision,
                top + pixelHeight * j + pixelHeight * horizontalPrecision,
                fill=rgbToHex(*pixel[:3]),
                outline="",
                tags="delete"
            )