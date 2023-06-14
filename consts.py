from tkinter import Toplevel, Canvas, Tk
from math import tan, radians
from map import map

debug = True

root = Tk()

screenD = None
screenDScale = None
if debug:
    rootD = Toplevel()
    screenD = Canvas(rootD, width=400, height=400, background="black")
    screenD.length = 400
    screenD.pack()
    screenDScale = screenD.length / (64 * len(map()))

# root.configure(cursor="none")

screen = Canvas(root, width=960, height=540, background="black")

screen.width = 960
screen.height = 540
fov = 85
screen.depth = (screen.width / 2) / tan(radians(fov / 2))

fps = 30

verticalPrecision = 10
horizontalPrecision = 1

screen.pack()
screen.focus_set()