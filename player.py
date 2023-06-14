from dataclasses import dataclass
from raycaster import Ray
from consts import fov, screen, verticalPrecision
from math import cos, sin, radians
from map import map, mapInfo

angles = {
    "w": 1,
    "a": -1,
    "s": -1,
    "d": 1
}

@dataclass
class Player:
    x: float
    y: float
    z: float
    rot: float
    speed: float
    rotSpeed: float
    loadFrame: int = 0
    def __post_init__(self):
        self.rays = [Ray(fov / screen.width * i - fov / 2) for i in range(0, screen.width, verticalPrecision)]
        self.moveKeys = []
        self.toRotate = 0
        self.crouch = False

    def move(self):
        if len(self.moveKeys):
            forwards = 0
            lateral = 0
            for i in self.moveKeys:
                if i in ["w", "s"]:
                    forwards += angles[i]
                else:
                    lateral += angles[i]

            match (forwards, lateral):
                case (1, 0):
                    angle = 0
                case (1, 1):
                    angle = 45
                case (0, 1):
                    angle = 90
                case (-1, 1):
                    angle = 135
                case (-1, 0):
                    angle = 180
                case (-1, -1):
                    angle = 225
                case (0, -1):
                    angle = 270
                case (1, -1):
                    angle = 315
                case _:
                    angle = None

            if angle != None:
                angle = (angle - self.rot) % 360
    
                deltaY = cos(radians(angle)) * self.speed
                deltaX = -sin(radians(angle)) * self.speed

                if not map()[round((self.y + deltaY) // 64)][round(self.x // 64)]:
                    self.y += deltaY
                if not map()[round(self.y // 64)][round((self.x + deltaX) // 64)]:
                    self.x += deltaX

        self.rot = (self.rot - self.toRotate * self.rotSpeed) % 360
            

player = Player(mapInfo()[1][0]*64 + 8, mapInfo()[1][1]*64 + 32, 32, 90, 8, 15)