import tkinter as tk

w, h = 600, 600
win = tk.Tk()
squareSize = 20

canvas = tk.Canvas(width=w, height=h)

def make_cell(event):
    id = canvas.find_withtag("current")[0]
    canvas.itemconfig(id, fill='yellow', tags="cell")

def make_empty(event):
    id = canvas.find_withtag("current")[0]
    canvas.itemconfig(id, fill='black', tags="blank")

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
        canvas.itemconfig(to_delete[d], fill='black')
    for f in range(0, len(to_fill)):
        canvas.itemconfig(to_fill[f], fill='yellow')

scene()

next = tk.Button(win, text='Next step', command=run)
l = tk.Label(win, text = "L mouse - add cell | R mouse - remove cell | Next step - plays one step of simulation")
l.pack()
next.pack()


canvas.tag_bind("blank", "<Button-1>", make_cell)
canvas.tag_bind("cell", "<Button-3>", make_empty)
canvas.pack()
win.mainloop()
