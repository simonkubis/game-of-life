import tkinter as tk
from tkinter.filedialog import askopenfile

w, h = 600, 600
win = tk.Tk()
squareSize = 60

canvas = tk.Canvas(width=w, height=h)

def make_cell(event):
    id = canvas.find_withtag("current")[0]
    canvas.itemconfig(id, fill='yellow', tags="cell")


def get_neighbours(id):
        line = w/squareSize
        total = line*(h/squareSize)
        items = [int(id-line-1), int(id - line), int(id - line + 1), int(id - 1), int(id + 1), int(id + line - 1), int(id + line), int(id + line + 1)]
        
        if(id <= line):
            items = replaceItems([0,1,2], items)
        if(id > total-line):
            items = replaceItems([5,6,7], items)
        if((id-1)%line == 0):
            items = replaceItems([0,3,5], items)
        if((id)%line == 0):
            items = replaceItems([2,4,7], items)

        colors = []
        for i in range(0, len(items)):
            colors.append(canvas.itemcget(items[i], "fill"))
        return colors

def replaceItems(indexes, list):
    for i in range(0, len(indexes)):
        list[indexes[i]] = -20
    return list

def scene():
    for y in range(0, int(h / squareSize)):
        for x in range(0, int(w / squareSize)):
            canvas.create_rectangle(x*squareSize, y*squareSize, squareSize + x*squareSize, squareSize + y*squareSize,fill="black", outline="white", tags="blank")

def run():
    to_fill = []
    to_delete = []
    for i in range(0, int((w/squareSize)*(h/squareSize))):
        data = get_neighbours(i)
        if(data.count("yellow") == 3):
            to_fill.append(i)
        if(canvas.itemcget(i, "fill") == "yellow"):
            if(data.count("yellow") < 2 or data.count("yellow") > 3):
                to_delete.append(i)
    for d in range(0, len(to_delete)):
        canvas.itemconfig(to_delete[d], fill='black', tags="blank")
    for f in range(0, len(to_fill)):
        canvas.itemconfig(to_fill[f], fill='yellow', tags="cell")

scene()


def open_file():
    positions = ''
    file = askopenfile(parent=win, mode='rb', title="Choose a text file", filetypes=[("File", "*.txt")])
    if file:
       for line in file:
           temp = str(line.strip())
           positions += temp.split("b'")[1].split("'")[0]
    for i in range(0, len(positions)):
        char = positions[i]
        if(char == "1"):
            canvas.itemconfig(i + 1, fill='yellow', tags="cell")


next = tk.Button(win, text='Next step', command=run)
#play = tk.Button(win, text='Play', command=play)
open = tk.Button(win, text='Open a file', command=open_file)
open.pack()
#play.pack()
next.pack()


canvas.tag_bind("blank", "<Button-1>", make_cell)
canvas.pack()
win.mainloop()
