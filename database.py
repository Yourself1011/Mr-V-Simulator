from json import loads, dumps
from consts import osName, screen, nameInput
import tkinter

try:
    with open("./database.txt", "r+") as f:
        raw = f.read().replace("'", "\"")
        unsorted = loads(raw)
        highscores = sorted(unsorted, key=lambda x: x[1], reverse=True)

except FileNotFoundError as e:
    print(str(e) + "\nCouldn't open database, creating one for you")
    
    with open("./database.txt", "w") as f:
        f.write("[('',0)]")
    unsorted = [('',0)]
    highscores = unsorted

submitted = False
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
            print("SLDKFJ")
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
    unsorted.append((nameInput.get(), inputScore))
    highscores = sorted(unsorted, key=lambda x: x[1], reverse=True)
    
    with open("./database.txt", "w") as f:
        f.write(dumps(unsorted))
        
    screen.delete("score")
    submitted=True
